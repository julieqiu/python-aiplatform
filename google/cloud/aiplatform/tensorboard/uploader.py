# -*- coding: utf-8 -*-

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Uploads a TensorBoard logdir to TensorBoard.gcp."""

import abc
from collections import defaultdict
import functools
import logging
import os
import re
import time
from typing import ContextManager, Dict, FrozenSet, Generator, Iterable, Optional, Tuple
import uuid

from google.api_core import exceptions
from google.cloud import storage
from google.cloud.aiplatform import base
from google.cloud.aiplatform.compat.services import (
    tensorboard_service_client,
)
from google.cloud.aiplatform.compat.types import tensorboard_data
from google.cloud.aiplatform.compat.types import tensorboard_experiment
from google.cloud.aiplatform.compat.types import tensorboard_service
from google.cloud.aiplatform.compat.types import tensorboard_time_series
from google.cloud.aiplatform.tensorboard import logdir_loader
from google.cloud.aiplatform.tensorboard import upload_tracker
from google.cloud.aiplatform.tensorboard import uploader_constants
from google.cloud.aiplatform.tensorboard import uploader_utils
from google.cloud.aiplatform.tensorboard.plugins.tf_profiler import (
    profile_uploader,
)
import grpc
import tensorflow as tf

from google.protobuf import timestamp_pb2 as timestamp
from google.protobuf import message
from tensorboard.backend import process_graph
from tensorboard.backend.event_processing.plugin_event_accumulator import (
    directory_loader,
)
from tensorboard.backend.event_processing.plugin_event_accumulator import (
    event_file_loader,
)
from tensorboard.backend.event_processing.plugin_event_accumulator import (
    io_wrapper,
)
from tensorboard.compat.proto import graph_pb2
from tensorboard.compat.proto import summary_pb2
from tensorboard.compat.proto import types_pb2
from tensorboard.plugins.graph import metadata as graph_metadata
from tensorboard.uploader.proto import server_info_pb2
from tensorboard.util import tb_logging
from tensorboard.util import tensor_util

_LOGGER = base.Logger(__name__)

TensorboardServiceClient = tensorboard_service_client.TensorboardServiceClient

logger = tb_logging.get_logger()
logger.setLevel(logging.WARNING)


class RequestSender(object):
    """A base class for additional request sender objects.

    Currently just used for typing.
    """

    pass


class TensorBoardUploader(object):
    """Uploads a TensorBoard logdir to TensorBoard.gcp."""

    def __init__(
        self,
        experiment_name: str,
        tensorboard_resource_name: str,
        blob_storage_bucket: storage.Bucket,
        blob_storage_folder: str,
        writer_client: TensorboardServiceClient,
        logdir: str,
        allowed_plugins: FrozenSet[str],
        experiment_display_name: Optional[str] = None,
        upload_limits: Optional[server_info_pb2.UploadLimits] = None,
        logdir_poll_rate_limiter: Optional[uploader_utils.RateLimiter] = None,
        rpc_rate_limiter: Optional[uploader_utils.RateLimiter] = None,
        tensor_rpc_rate_limiter: Optional[uploader_utils.RateLimiter] = None,
        blob_rpc_rate_limiter: Optional[uploader_utils.RateLimiter] = None,
        description: Optional[str] = None,
        verbosity: int = 1,
        one_shot: bool = False,
        event_file_inactive_secs: Optional[int] = None,
        run_name_prefix=None,
    ):
        """Constructs a TensorBoardUploader.

        Args:
          experiment_name: Name of this experiment. Unique to the given
            tensorboard_resource_name.
          tensorboard_resource_name: Name of the Tensorboard resource with this
            format
            projects/{project}/locations/{location}/tensorboards/{tensorboard}
          writer_client: a TensorBoardWriterService stub instance
          logdir: path of the log directory to upload
          experiment_display_name: The display name of the experiment.
          allowed_plugins: collection of string plugin names; events will only be
            uploaded if their time series's metadata specifies one of these plugin
            names
          upload_limits: instance of tensorboard.service.UploadLimits proto.
          logdir_poll_rate_limiter: a `RateLimiter` to use to limit logdir polling
            frequency, to avoid thrashing disks, especially on networked file
            systems
          rpc_rate_limiter: a `RateLimiter` to use to limit write RPC frequency.
            Note this limit applies at the level of single RPCs in the Scalar and
            Tensor case, but at the level of an entire blob upload in the Blob
            case-- which may require a few preparatory RPCs and a stream of chunks.
            Note the chunk stream is internally rate-limited by backpressure from
            the server, so it is not a concern that we do not explicitly rate-limit
            within the stream here.
          description: String description to assign to the experiment.
          verbosity: Level of verbosity, an integer. Supported value: 0 - No upload
            statistics is printed. 1 - Print upload statistics while uploading data
            (default).
          one_shot: Once uploading starts, upload only the existing data in the
            logdir and then return immediately, instead of the default behavior of
            continuing to listen for new data in the logdir and upload them when it
            appears.
          event_file_inactive_secs: Age in seconds of last write after which an
            event file is considered inactive. If none then event file is never
            considered inactive.
          run_name_prefix: If present, all runs created by this invocation will have
            their name prefixed by this value.
        """
        self._experiment_name = experiment_name
        self._experiment_display_name = experiment_display_name
        self._tensorboard_resource_name = tensorboard_resource_name
        self._blob_storage_bucket = blob_storage_bucket
        self._blob_storage_folder = blob_storage_folder
        self._api = writer_client
        self._logdir = logdir
        self._allowed_plugins = frozenset(allowed_plugins)
        self._run_name_prefix = run_name_prefix
        self._is_brand_new_experiment = False
        self._continue_uploading = True

        self._upload_limits = upload_limits
        if not self._upload_limits:
            self._upload_limits = server_info_pb2.UploadLimits()
            self._upload_limits.max_scalar_request_size = (
                uploader_constants.DEFAULT_MAX_SCALAR_REQUEST_SIZE
            )
            self._upload_limits.min_scalar_request_interval = (
                uploader_constants.DEFAULT_MIN_SCALAR_REQUEST_INTERVAL
            )
            self._upload_limits.min_tensor_request_interval = (
                uploader_constants.DEFAULT_MIN_TENSOR_REQUEST_INTERVAL
            )
            self._upload_limits.max_tensor_request_size = (
                uploader_constants.DEFAULT_MAX_TENSOR_REQUEST_SIZE
            )
            self._upload_limits.max_tensor_point_size = (
                uploader_constants.DEFAULT_MAX_TENSOR_POINT_SIZE
            )
            self._upload_limits.min_blob_request_interval = (
                uploader_constants.DEFAULT_MIN_BLOB_REQUEST_INTERVAL
            )
            self._upload_limits.max_blob_request_size = (
                uploader_constants.DEFAULT_MAX_BLOB_REQUEST_SIZE
            )
            self._upload_limits.max_blob_size = uploader_constants.DEFAULT_MAX_BLOB_SIZE
        self._description = description
        self._verbosity = verbosity
        self._one_shot = one_shot
        self._dispatcher = None
        self._additional_senders: Dict[str, uploader_utils.RequestSender] = {}
        if logdir_poll_rate_limiter is None:
            self._logdir_poll_rate_limiter = uploader_utils.RateLimiter(
                uploader_constants.MIN_LOGDIR_POLL_INTERVAL_SECS
            )
        else:
            self._logdir_poll_rate_limiter = logdir_poll_rate_limiter

        if rpc_rate_limiter is None:
            self._rpc_rate_limiter = uploader_utils.RateLimiter(
                self._upload_limits.min_scalar_request_interval / 1000
            )
        else:
            self._rpc_rate_limiter = rpc_rate_limiter

        if tensor_rpc_rate_limiter is None:
            self._tensor_rpc_rate_limiter = uploader_utils.RateLimiter(
                self._upload_limits.min_tensor_request_interval / 1000
            )
        else:
            self._tensor_rpc_rate_limiter = tensor_rpc_rate_limiter

        if blob_rpc_rate_limiter is None:
            self._blob_rpc_rate_limiter = uploader_utils.RateLimiter(
                self._upload_limits.min_blob_request_interval / 1000
            )
        else:
            self._blob_rpc_rate_limiter = blob_rpc_rate_limiter

        def active_filter(secs):
            return (
                not bool(event_file_inactive_secs)
                or secs + event_file_inactive_secs >= time.time()
            )

        directory_loader_factory = functools.partial(
            directory_loader.DirectoryLoader,
            loader_factory=event_file_loader.TimestampedEventFileLoader,
            path_filter=io_wrapper.IsTensorFlowEventsFile,
            active_filter=active_filter,
        )
        self._logdir_loader = logdir_loader.LogdirLoader(
            self._logdir, directory_loader_factory
        )
        self._logdir_loader_pre_create = logdir_loader.LogdirLoader(
            self._logdir, directory_loader_factory
        )
        self._tracker = upload_tracker.UploadTracker(verbosity=self._verbosity)

        self._create_additional_senders()

    def _create_or_get_experiment(self) -> tensorboard_experiment.TensorboardExperiment:
        """Create an experiment or get an experiment.

        Attempts to create an experiment. If the experiment already exists and
        creation fails then the experiment will be retrieved.

        Returns:
          The created or retrieved experiment.
        """
        logger.info("Creating experiment")

        tb_experiment = tensorboard_experiment.TensorboardExperiment(
            description=self._description, display_name=self._experiment_display_name
        )

        try:
            experiment = self._api.create_tensorboard_experiment(
                parent=self._tensorboard_resource_name,
                tensorboard_experiment=tb_experiment,
                tensorboard_experiment_id=self._experiment_name,
            )
            self._is_brand_new_experiment = True
        except exceptions.AlreadyExists:
            logger.info("Creating experiment failed. Retrieving experiment.")
            experiment_name = os.path.join(
                self._tensorboard_resource_name, "experiments", self._experiment_name
            )
            experiment = self._api.get_tensorboard_experiment(name=experiment_name)
        return experiment

    def create_experiment(self):
        """Creates an Experiment for this upload session and returns the ID."""

        experiment = self._create_or_get_experiment()
        self._experiment = experiment
        self._one_platform_resource_manager = uploader_utils.OnePlatformResourceManager(
            self._experiment.name, self._api
        )

        self._request_sender = _BatchedRequestSender(
            self._experiment.name,
            self._api,
            allowed_plugins=self._allowed_plugins,
            upload_limits=self._upload_limits,
            rpc_rate_limiter=self._rpc_rate_limiter,
            tensor_rpc_rate_limiter=self._tensor_rpc_rate_limiter,
            blob_rpc_rate_limiter=self._blob_rpc_rate_limiter,
            blob_storage_bucket=self._blob_storage_bucket,
            blob_storage_folder=self._blob_storage_folder,
            one_platform_resource_manager=self._one_platform_resource_manager,
            tracker=self._tracker,
        )

        # Update partials with experiment name
        for sender in self._additional_senders.keys():
            self._additional_senders[sender] = self._additional_senders[sender](
                experiment_resource_name=self._experiment.name,
            )

        self._dispatcher = _Dispatcher(
            request_sender=self._request_sender,
            additional_senders=self._additional_senders,
        )

    def _should_profile(self) -> bool:
        """Indicate if profile plugin should be enabled."""
        if "profile" in self._allowed_plugins:
            logger.info("Profile plugin is enabled.")
            return True
        return False

    def _create_additional_senders(self) -> Dict[str, uploader_utils.RequestSender]:
        """Create any additional senders for non traditional event files.

        Some items that are used for plugins do not process typical event files,
        but need to be searched for and stored so that they can be used by the
        plugin. If there are any items that cannot be searched for via the
        `_BatchedRequestSender`, add them here.
        """
        if self._should_profile():
            source_bucket = uploader_utils.get_source_bucket(self._logdir)

            self._additional_senders["profile"] = functools.partial(
                profile_uploader.ProfileRequestSender,
                api=self._api,
                upload_limits=self._upload_limits,
                blob_rpc_rate_limiter=self._blob_rpc_rate_limiter,
                blob_storage_bucket=self._blob_storage_bucket,
                blob_storage_folder=self._blob_storage_folder,
                source_bucket=source_bucket,
                tracker=self._tracker,
                logdir=self._logdir,
            )

    def get_experiment_resource_name(self):
        return self._experiment.name

    def start_uploading(self):
        """Blocks forever to continuously upload data from the logdir.

        Raises:
          RuntimeError: If `create_experiment` has not yet been called.
          ExperimentNotFoundError: If the experiment is deleted during the
            course of the upload.
        """
        if self._dispatcher is None:
            raise RuntimeError("Must call create_experiment() before start_uploading()")

        if self._one_shot:
            if self._is_brand_new_experiment:
                self._pre_create_runs_and_time_series()
            else:
                logger.warning(
                    "Please consider uploading to a new experiment instead of "
                    "an existing one, as the former allows for better upload "
                    "performance."
                )

        while self._continue_uploading:
            self._logdir_poll_rate_limiter.tick()
            self._upload_once()
            if self._one_shot:
                break
        if self._one_shot and not self._tracker.has_data():
            logger.warning(
                "One-shot mode was used on a logdir (%s) without any uploadable data"
                % self._logdir
            )

    def _end_uploading(self):
        self._continue_uploading = False

    def _pre_create_runs_and_time_series(self):
        """Iterates though the log dir to collect TensorboardRuns and
        TensorboardTimeSeries that need to be created, and creates them in batch
        to speed up uploading later on.
        """
        self._logdir_loader_pre_create.synchronize_runs()
        run_to_events = self._logdir_loader_pre_create.get_run_events()
        if self._run_name_prefix:
            run_to_events = {
                self._run_name_prefix + k: v for k, v in run_to_events.items()
            }

        run_names = []
        run_tag_name_to_time_series_proto = {}
        for (run_name, events) in run_to_events.items():
            run_names.append(run_name)
            for event in events:
                _filter_graph_defs(event)
                for value in event.summary.value:
                    metadata, is_valid = self._request_sender.get_metadata_and_validate(
                        run_name, value
                    )
                    if not is_valid:
                        continue
                    if metadata.data_class == summary_pb2.DATA_CLASS_SCALAR:
                        value_type = (
                            tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
                        )
                    elif metadata.data_class == summary_pb2.DATA_CLASS_TENSOR:
                        value_type = (
                            tensorboard_time_series.TensorboardTimeSeries.ValueType.TENSOR
                        )
                    elif metadata.data_class == summary_pb2.DATA_CLASS_BLOB_SEQUENCE:
                        value_type = (
                            tensorboard_time_series.TensorboardTimeSeries.ValueType.BLOB_SEQUENCE
                        )

                    run_tag_name_to_time_series_proto[
                        (run_name, value.tag)
                    ] = tensorboard_time_series.TensorboardTimeSeries(
                        display_name=value.tag,
                        value_type=value_type,
                        plugin_name=metadata.plugin_data.plugin_name,
                        plugin_data=metadata.plugin_data.content,
                    )

        self._one_platform_resource_manager.batch_create_runs(run_names)
        self._one_platform_resource_manager.batch_create_time_series(
            run_tag_name_to_time_series_proto
        )

    def _upload_once(self):
        """Runs one upload cycle, sending zero or more RPCs."""
        logger.info("Starting an upload cycle")

        sync_start_time = time.time()
        self._logdir_loader.synchronize_runs()
        sync_duration_secs = time.time() - sync_start_time
        logger.info("Logdir sync took %.3f seconds", sync_duration_secs)

        run_to_events = self._logdir_loader.get_run_events()
        if self._run_name_prefix:
            run_to_events = {
                self._run_name_prefix + k: v for k, v in run_to_events.items()
            }

        # Add a profile event to trigger send_request in _additional_senders
        if self._should_profile():
            run_to_events[self._run_name_prefix] = None

        with self._tracker.send_tracker():
            self._dispatcher.dispatch_requests(run_to_events)


class PermissionDeniedError(RuntimeError):
    pass


class ExperimentNotFoundError(RuntimeError):
    pass


class _OutOfSpaceError(Exception):
    """Action could not proceed without overflowing request budget.

    This is a signaling exception (like `StopIteration`) used internally
    by `_*RequestSender`; it does not mean that anything has gone wrong.
    """

    pass


class _BatchedRequestSender(object):
    """Helper class for building requests that fit under a size limit.

    This class maintains stateful request builders for each of the possible
    request types (scalars, tensors, and blobs).  These accumulate batches
    independently, each maintaining its own byte budget and emitting a request
    when the batch becomes full.  As a consequence, events of different types
    will likely be sent to the backend out of order.  E.g., in the extreme case,
    a single tensor-flavored request may be sent only when the event stream is
    exhausted, even though many more recent scalar events were sent earlier.

    This class is not threadsafe. Use external synchronization if
    calling its methods concurrently.
    """

    def __init__(
        self,
        experiment_resource_name: str,
        api: TensorboardServiceClient,
        allowed_plugins: Iterable[str],
        upload_limits: server_info_pb2.UploadLimits,
        rpc_rate_limiter: uploader_utils.RateLimiter,
        tensor_rpc_rate_limiter: uploader_utils.RateLimiter,
        blob_rpc_rate_limiter: uploader_utils.RateLimiter,
        blob_storage_bucket: storage.Bucket,
        blob_storage_folder: str,
        one_platform_resource_manager: uploader_utils.OnePlatformResourceManager,
        tracker: upload_tracker.UploadTracker,
    ):
        """Constructs _BatchedRequestSender for the given experiment resource.

        Args:
          experiment_resource_name: Name of the experiment resource of the form
            projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}
          api: Tensorboard service stub used to interact with experiment resource.
          allowed_plugins: The plugins supported by the Tensorboard.gcp resource.
          upload_limits: Upload limits for for api calls.
          rpc_rate_limiter: a `RateLimiter` to use to limit write RPC frequency.
            Note this limit applies at the level of single RPCs in the Scalar and
            Tensor case, but at the level of an entire blob upload in the Blob
            case-- which may require a few preparatory RPCs and a stream of chunks.
            Note the chunk stream is internally rate-limited by backpressure from
            the server, so it is not a concern that we do not explicitly rate-limit
            within the stream here.
          one_platform_resource_manager: An instance of the One Platform
            resource management class.
          tracker: Upload tracker to track information about uploads.
        """
        self._experiment_resource_name = experiment_resource_name
        self._api = api
        self._tag_metadata = {}
        self._allowed_plugins = frozenset(allowed_plugins)
        self._tracker = tracker
        self._one_platform_resource_manager = one_platform_resource_manager
        self._scalar_request_sender = _ScalarBatchedRequestSender(
            experiment_resource_id=experiment_resource_name,
            api=api,
            rpc_rate_limiter=rpc_rate_limiter,
            max_request_size=upload_limits.max_scalar_request_size,
            tracker=self._tracker,
            one_platform_resource_manager=self._one_platform_resource_manager,
        )
        self._tensor_request_sender = _TensorBatchedRequestSender(
            experiment_resource_id=experiment_resource_name,
            api=api,
            rpc_rate_limiter=tensor_rpc_rate_limiter,
            max_request_size=upload_limits.max_tensor_request_size,
            max_tensor_point_size=upload_limits.max_tensor_point_size,
            tracker=self._tracker,
            one_platform_resource_manager=self._one_platform_resource_manager,
        )
        self._blob_request_sender = _BlobRequestSender(
            experiment_resource_id=experiment_resource_name,
            api=api,
            rpc_rate_limiter=blob_rpc_rate_limiter,
            max_blob_request_size=upload_limits.max_blob_request_size,
            max_blob_size=upload_limits.max_blob_size,
            blob_storage_bucket=blob_storage_bucket,
            blob_storage_folder=blob_storage_folder,
            tracker=self._tracker,
            one_platform_resource_manager=self._one_platform_resource_manager,
        )

    def send_request(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
    ):
        """Accepts a stream of TF events and sends batched write RPCs.

        Each sent request will be batched, the size of each batch depending on
        the type of data (Scalar vs Tensor vs Blob) being sent.

        Args:
          run_name: Name of the run retrieved by `LogdirLoader.get_run_events`
          event: The `tf.compat.v1.Event` for the run
          value: A single `tf.compat.v1.Summary.Value` from the event, where
            there can be multiple values per event.

        Raises:
          RuntimeError: If no progress can be made because even a single
          point is too large (say, due to a gigabyte-long tag name).
        """
        metadata, is_valid = self.get_metadata_and_validate(run_name, value)
        if not is_valid:
            return
        plugin_name = metadata.plugin_data.plugin_name
        self._tracker.add_plugin_name(plugin_name)

        if metadata.data_class == summary_pb2.DATA_CLASS_SCALAR:
            self._scalar_request_sender.add_event(run_name, event, value, metadata)
        elif metadata.data_class == summary_pb2.DATA_CLASS_TENSOR:
            self._tensor_request_sender.add_event(run_name, event, value, metadata)
        elif metadata.data_class == summary_pb2.DATA_CLASS_BLOB_SEQUENCE:
            self._blob_request_sender.add_event(run_name, event, value, metadata)

    def flush(self):
        """Flushes any events that have been stored."""
        self._scalar_request_sender.flush()
        self._tensor_request_sender.flush()
        self._blob_request_sender.flush()

    def get_metadata_and_validate(
        self, run_name: str, value: tf.compat.v1.Summary.Value
    ) -> Tuple[tf.compat.v1.SummaryMetadata, bool]:
        """

        :param run_name: Name of the run retrieved by
        `LogdirLoader.get_run_events`
        :param value: A single `tf.compat.v1.Summary.Value` from the event,
        where there can be multiple values per event.
        :return: (metadata, is_valid): a metadata derived from the value, and
        whether the value itself is valid.
        """

        time_series_key = (run_name, value.tag)

        # The metadata for a time series is memorized on the first event.
        # If later events arrive with a mismatching plugin_name, they are
        # ignored with a warning.
        metadata = self._tag_metadata.get(time_series_key)
        first_in_time_series = False
        if metadata is None:
            first_in_time_series = True
            metadata = value.metadata
            self._tag_metadata[time_series_key] = metadata

        plugin_name = metadata.plugin_data.plugin_name
        if value.HasField("metadata") and (
            plugin_name != value.metadata.plugin_data.plugin_name
        ):
            logger.warning(
                "Mismatching plugin names for %s.  Expected %s, found %s.",
                time_series_key,
                metadata.plugin_data.plugin_name,
                value.metadata.plugin_data.plugin_name,
            )
            return metadata, False
        if plugin_name not in self._allowed_plugins:
            if first_in_time_series:
                logger.info(
                    "Skipping time series %r with unsupported plugin name %r",
                    time_series_key,
                    plugin_name,
                )
            return metadata, False
        return metadata, True


class _Dispatcher(object):
    """Dispatch the requests to the correct request senders."""

    def __init__(
        self,
        request_sender: _BatchedRequestSender,
        additional_senders: Optional[Dict[str, uploader_utils.RequestSender]] = None,
    ):
        """Construct a _Dispatcher object for the TensorboardUploader.

        Args:
            request_sender: A `_BatchedRequestSender` for handling events.
            additional_senders: A dictionary mapping a plugin name to additional
              Senders.
        """
        self._request_sender = request_sender

        if not additional_senders:
            additional_senders = {}
        self._additional_senders = additional_senders

    def _dispatch_additional_senders(
        self,
        run_name: str,
    ):
        """Dispatch events to any additional senders.

        These senders process non traditional event files for a specific plugin
        and use a send_request function to process events.

        Args:
            run_name: String of current training run
        """
        for key, sender in self._additional_senders.items():
            sender.send_request(run_name)

    def dispatch_requests(
        self, run_to_events: Dict[str, Generator[tf.compat.v1.Event, None, None]]
    ):
        """Routes events to the appropriate sender.

        Takes a mapping from strings to an event generator. The function routes
        any events that should be handled by the `_BatchedRequestSender` and
        non-traditional events that need to be handled differently, which are
        stored as "_additional_senders". The `_request_sender` is then flushed
        after all events are added.

        Note that `dataclass_compat` may emit multiple variants of
        the same event, for backwards compatibility.  Thus this stream should
        be filtered to obtain the desired version of each event.  Here, we
        ignore any event that does not have a `summary` field.

        Furthermore, the events emitted here could contain values that do not
        have `metadata.data_class` set; these too should be ignored.  In
        `_send_summary_value(...)` above, we switch on `metadata.data_class`
        and drop any values with an unknown (i.e., absent or unrecognized)
        `data_class`.

        Args:
          run_to_events: Mapping from run name to generator of `tf.compat.v1.Event`
            values, as returned by `LogdirLoader.get_run_events`.
        """
        for (run_name, events) in run_to_events.items():
            self._dispatch_additional_senders(run_name)
            if events is not None:
                for event in events:
                    _filter_graph_defs(event)
                    for value in event.summary.value:
                        self._request_sender.send_request(run_name, event, value)
        self._request_sender.flush()


class _BaseBatchedRequestSender(object):
    """Helper class for building requests that fit under a size limit.

    This class accumulates a current request.  `add_event(...)` may or may not
    send the request (and start a new one).  After all `add_event(...)` calls
    are complete, a final call to `flush()` is needed to send the final request.

    This class is not threadsafe. Use external synchronization if calling its
    methods concurrently.
    """

    def __init__(
        self,
        experiment_resource_id: str,
        api: TensorboardServiceClient,
        rpc_rate_limiter: uploader_utils.RateLimiter,
        max_request_size: int,
        tracker: upload_tracker.UploadTracker,
        one_platform_resource_manager: uploader_utils.OnePlatformResourceManager,
    ):
        """Constructor for _BaseBatchedRequestSender.

        Args:
          experiment_resource_id: The resource id for the experiment with the following format
            projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}
          api: TensorboardServiceStub
          rpc_rate_limiter: uploader_utils.RateLimiter to limit rate of this request sender
          max_request_size: max number of bytes to send
          tracker:
        """
        self._experiment_resource_id = experiment_resource_id
        self._api = api
        self._rpc_rate_limiter = rpc_rate_limiter
        self._byte_budget_manager = _ByteBudgetManager(max_request_size)
        self._tracker = tracker
        self._one_platform_resource_manager = one_platform_resource_manager

        # cache: map from Tensorboard tag to TimeSeriesData
        # cleared whenever a new request is created
        self._run_to_tag_to_time_series_data: Dict[
            str, Dict[str, tensorboard_data.TimeSeriesData]
        ] = defaultdict(defaultdict)
        self._new_request()

    def _new_request(self):
        """Allocates a new request and refreshes the budget."""
        self._request = tensorboard_service.WriteTensorboardExperimentDataRequest(
            tensorboard_experiment=self._experiment_resource_id
        )
        self._run_to_tag_to_time_series_data.clear()
        self._num_values = 0
        self._byte_budget_manager.reset(self._request)

    def add_event(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ):
        """Attempts to add the given event to the current request.

        If the event cannot be added to the current request because the byte
        budget is exhausted, the request is flushed, and the event is added
        to the next request.

        Args:
          event: The tf.compat.v1.Event event containing the value.
          value: A scalar tf.compat.v1.Summary.Value.
          metadata: SummaryMetadata of the event.
        """
        try:
            self._add_event_internal(run_name, event, value, metadata)
        except _OutOfSpaceError:
            self.flush()
            # Try again.  This attempt should never produce OutOfSpaceError
            # because we just flushed.
            try:
                self._add_event_internal(run_name, event, value, metadata)
            except _OutOfSpaceError:
                raise RuntimeError("add_event failed despite flush")

    def _add_event_internal(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ):
        self._num_values += 1
        time_series_data_proto = self._run_to_tag_to_time_series_data[run_name].get(
            value.tag
        )
        if time_series_data_proto is None:
            time_series_data_proto = self._create_time_series_data(
                run_name, value.tag, metadata
            )
        self._create_point(run_name, time_series_data_proto, event, value, metadata)

    def flush(self):
        """Sends the active request after removing empty runs and tags.

        Starts a new, empty active request.
        """
        request = self._request
        has_data = False
        for (
            run_name,
            tag_to_time_series_data,
        ) in self._run_to_tag_to_time_series_data.items():
            r = tensorboard_service.WriteTensorboardRunDataRequest(
                tensorboard_run=self._one_platform_resource_manager.get_run_resource_name(
                    run_name
                )
            )
            r.time_series_data = list(tag_to_time_series_data.values())
            _prune_empty_time_series(r)
            if not r.time_series_data:
                continue
            request.write_run_data_requests.extend([r])
            has_data = True

        if not has_data:
            return

        self._rpc_rate_limiter.tick()

        with uploader_utils.request_logger(request):
            with self._get_tracker():
                try:
                    self._api.write_tensorboard_experiment_data(
                        tensorboard_experiment=request.tensorboard_experiment,
                        write_run_data_requests=request.write_run_data_requests,
                    )
                except grpc.RpcError as e:
                    if (
                        hasattr(e, "code")
                        and getattr(e, "code")() == grpc.StatusCode.NOT_FOUND
                    ):
                        raise ExperimentNotFoundError() from e
                    logger.error("Upload call failed with error %s", e)

        self._new_request()

    def _create_time_series_data(
        self, run_name: str, tag_name: str, metadata: tf.compat.v1.SummaryMetadata
    ) -> tensorboard_data.TimeSeriesData:
        """Adds a time_series for the tag_name, if there's space.

        Args:
          tag_name: String name of the tag to add (as `value.tag`).

        Returns:
          The TimeSeriesData in _request proto with the given tag name.

        Raises:
          _OutOfSpaceError: If adding the tag would exceed the remaining
            request budget.
        """
        time_series_resource_name = (
            self._one_platform_resource_manager.get_time_series_resource_name(
                run_name,
                tag_name,
                lambda: tensorboard_time_series.TensorboardTimeSeries(
                    display_name=tag_name,
                    value_type=self._value_type,
                    plugin_name=metadata.plugin_data.plugin_name,
                    plugin_data=metadata.plugin_data.content,
                ),
            )
        )

        time_series_data_proto = tensorboard_data.TimeSeriesData(
            tensorboard_time_series_id=time_series_resource_name.split("/")[-1],
            value_type=self._value_type,
        )

        self._byte_budget_manager.add_time_series(time_series_data_proto)
        self._run_to_tag_to_time_series_data[run_name][
            tag_name
        ] = time_series_data_proto
        return time_series_data_proto

    def _create_point(
        self,
        run_name: str,
        time_series_proto: tensorboard_data.TimeSeriesData,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ):
        """Adds a scalar point to the given tag, if there's space.

        Args:
          time_series_proto: TimeSeriesData proto to which to add a point.
          event: Enclosing `Event` proto with the step and wall time data.
          value: `Summary.Value` proto.
          metadata: SummaryMetadata of the event.

        Raises:
          _OutOfSpaceError: If adding the point would exceed the remaining
            request budget.
        """
        point = self._create_data_point(run_name, event, value, metadata)

        if not self._validate(point, event, value):
            return

        time_series_proto.values.extend([point])
        try:
            self._byte_budget_manager.add_point(point)
        except _OutOfSpaceError:
            time_series_proto.values.pop()
            raise

    @abc.abstractmethod
    def _get_tracker(self) -> ContextManager:
        """
        :return: tracker function from upload_tracker.UploadTracker
        """
        pass

    @property
    @classmethod
    @abc.abstractmethod
    def _value_type(
        cls,
    ) -> tensorboard_time_series.TensorboardTimeSeries.ValueType:
        """
        :return: Value type of the time series.
        """
        pass

    @abc.abstractmethod
    def _create_data_point(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ) -> tensorboard_data.TimeSeriesDataPoint:
        """
        Creates data point protos for sending to the OnePlatform API.
        """
        pass

    def _validate(
        self,
        point: tensorboard_data.TimeSeriesDataPoint,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
    ):
        """
        Validations performed before including the data point to be sent to the
        OnePlatform API.
        """
        return True


class _ScalarBatchedRequestSender(_BaseBatchedRequestSender):
    """Helper class for building requests that fit under a size limit.

    This class accumulates a current request.  `add_event(...)` may or may not
    send the request (and start a new one).  After all `add_event(...)` calls
    are complete, a final call to `flush()` is needed to send the final request.

    This class is not threadsafe. Use external synchronization if calling its
    methods concurrently.
    """

    _value_type = tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR

    def __init__(
        self,
        experiment_resource_id: str,
        api: TensorboardServiceClient,
        rpc_rate_limiter: uploader_utils.RateLimiter,
        max_request_size: int,
        tracker: upload_tracker.UploadTracker,
        one_platform_resource_manager: uploader_utils.OnePlatformResourceManager,
    ):
        """Constructor for _ScalarBatchedRequestSender.

        Args:
          experiment_resource_id: The resource id for the experiment with the following format
            projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}
          api: TensorboardServiceStub
          rpc_rate_limiter: uploader_utils.RateLimiter to limit rate of this request sender
          max_request_size: max number of bytes to send
          tracker:
        """
        super().__init__(
            experiment_resource_id,
            api,
            rpc_rate_limiter,
            max_request_size,
            tracker,
            one_platform_resource_manager,
        )

    def _get_tracker(self) -> ContextManager:
        return self._tracker.scalars_tracker(self._num_values)

    def _create_data_point(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ) -> tensorboard_data.TimeSeriesDataPoint:
        scalar_proto = tensorboard_data.Scalar(
            value=tensor_util.make_ndarray(value.tensor).item()
        )
        return tensorboard_data.TimeSeriesDataPoint(
            step=event.step,
            scalar=scalar_proto,
            wall_time=timestamp.Timestamp(
                seconds=int(event.wall_time),
                nanos=int(round((event.wall_time % 1) * 10**9)),
            ),
        )


class _TensorBatchedRequestSender(_BaseBatchedRequestSender):
    """Helper class for building WriteTensor() requests that fit under a size limit.

    This class accumulates a current request.  `add_event(...)` may or may not
    send the request (and start a new one).  After all `add_event(...)` calls
    are complete, a final call to `flush()` is needed to send the final request.
    This class is not threadsafe. Use external synchronization if calling its
    methods concurrently.
    """

    _value_type = tensorboard_time_series.TensorboardTimeSeries.ValueType.TENSOR

    def __init__(
        self,
        experiment_resource_id: str,
        api: TensorboardServiceClient,
        rpc_rate_limiter: uploader_utils.RateLimiter,
        max_request_size: int,
        max_tensor_point_size: int,
        tracker: upload_tracker.UploadTracker,
        one_platform_resource_manager: uploader_utils.OnePlatformResourceManager,
    ):
        """Constructor for _TensorBatchedRequestSender.

        Args:
          experiment_resource_id: The resource id for the experiment with the following format
            projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}
          api: TensorboardServiceStub
          rpc_rate_limiter: uploader_utils.RateLimiter to limit rate of this request sender
          max_request_size: max number of bytes to send
          tracker:
        """
        super().__init__(
            experiment_resource_id,
            api,
            rpc_rate_limiter,
            max_request_size,
            tracker,
            one_platform_resource_manager,
        )
        self._max_tensor_point_size = max_tensor_point_size

    def _new_request(self):
        """Allocates a new request and refreshes the budget."""
        super()._new_request()
        self._num_values = 0
        self._num_values_skipped = 0
        self._tensor_bytes = 0
        self._tensor_bytes_skipped = 0

    def _get_tracker(self) -> ContextManager:
        return self._tracker.tensors_tracker(
            self._num_values,
            self._num_values_skipped,
            self._tensor_bytes,
            self._tensor_bytes_skipped,
        )

    def _create_data_point(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ) -> tensorboard_data.TimeSeriesDataPoint:
        return tensorboard_data.TimeSeriesDataPoint(
            step=event.step,
            tensor=tensorboard_data.TensorboardTensor(
                value=value.tensor.SerializeToString()
            ),
            wall_time=timestamp.Timestamp(
                seconds=int(event.wall_time),
                nanos=int(round((event.wall_time % 1) * 10**9)),
            ),
        )

    def _validate(
        self,
        point: tensorboard_data.TimeSeriesDataPoint,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
    ):
        self._num_values += 1
        tensor_size = len(point.tensor.value)
        self._tensor_bytes += tensor_size
        if tensor_size > self._max_tensor_point_size:
            logger.warning(
                "Tensor too large; skipping. " "Size %d exceeds limit of %d bytes.",
                tensor_size,
                self._max_tensor_point_size,
            )
            self._num_values_skipped += 1
            self._tensor_bytes_skipped += tensor_size
            return False

        try:
            tensor_util.make_ndarray(value.tensor)
        except ValueError as error:
            raise ValueError(
                "The uploader failed to upload a tensor. This seems to be "
                "due to a malformation in the tensor, which may be caused by "
                "a bug in the process that wrote the tensor.\n\n"
                "The tensor has tag '%s' and is at step %d and wall_time %.6f.\n\n"
                "Original error:\n%s" % (value.tag, event.step, event.wall_time, error)
            ) from error
        return True


class _ByteBudgetManager(object):
    """Helper class for managing the request byte budget for certain RPCs.

    This should be used for RPCs that organize data by Runs, Tags, and Points,
    specifically WriteScalar and WriteTensor.

    Any call to add_time_series() or add_point() may raise an
    _OutOfSpaceError, which is non-fatal. It signals to the caller that they
    should flush the current request and begin a new one.

    For more information on the protocol buffer encoding and how byte cost
    can be calculated, visit:

    https://developers.google.com/protocol-buffers/docs/encoding
    """

    def __init__(self, max_bytes: int):
        # The remaining number of bytes that we may yet add to the request.
        self._byte_budget = None  # type: int
        self._max_bytes = max_bytes

    def reset(
        self, base_request: tensorboard_service.WriteTensorboardExperimentDataRequest
    ):
        """Resets the byte budget and calculates the cost of the base request.

        Args:
          base_request: Base request.

        Raises:
          _OutOfSpaceError: If the size of the request exceeds the entire
            request byte budget.
        """
        self._byte_budget = self._max_bytes
        self._byte_budget -= (
            base_request._pb.ByteSize()
        )  # pylint: disable=protected-access
        if self._byte_budget < 0:
            raise _OutOfSpaceError("Byte budget too small for base request")

    def add_time_series(self, time_series_proto: tensorboard_data.TimeSeriesData):
        """Integrates the cost of a tag proto into the byte budget.

        Args:
          time_series_proto: The proto representing a time series.

        Raises:
          _OutOfSpaceError: If adding the time_series would exceed the remaining
          request budget.
        """
        cost = (
            # The size of the tag proto without any tag fields set.
            time_series_proto._pb.ByteSize()  # pylint: disable=protected-access
            # The size of the varint that describes the length of the tag
            # proto. We can't yet know the final size of the tag proto -- we
            # haven't yet set any point values -- so we can't know the final
            # size of this length varint. We conservatively assume it is maximum
            # size.
            + uploader_constants.MAX_VARINT64_LENGTH_BYTES
            # The size of the proto key.
            + 1
        )
        if cost > self._byte_budget:
            raise _OutOfSpaceError()
        self._byte_budget -= cost

    def add_point(self, point_proto: tensorboard_data.TimeSeriesDataPoint):
        """Integrates the cost of a point proto into the byte budget.

        Args:
          point_proto: The proto representing a point.

        Raises:
          _OutOfSpaceError: If adding the point would exceed the remaining request
           budget.
        """
        submessage_cost = point_proto._pb.ByteSize()  # pylint: disable=protected-access
        cost = (
            # The size of the point proto.
            submessage_cost
            # The size of the varint that describes the length of the point
            # proto.
            + _varint_cost(submessage_cost)
            # The size of the proto key.
            + 1
        )
        if cost > self._byte_budget:
            raise _OutOfSpaceError()
        self._byte_budget -= cost


class _BlobRequestSender(_BaseBatchedRequestSender):
    """Uploader for blob-type event data.

    Unlike the other types, this class does not accumulate events in batches;
    every blob is sent individually and immediately.  Nonetheless we retain
    the `add_event()`/`flush()` structure for symmetry.

    This class is not threadsafe. Use external synchronization if calling its
    methods concurrently.
    """

    _value_type = tensorboard_time_series.TensorboardTimeSeries.ValueType.BLOB_SEQUENCE

    def __init__(
        self,
        experiment_resource_id: str,
        api: TensorboardServiceClient,
        rpc_rate_limiter: uploader_utils.RateLimiter,
        max_blob_request_size: int,
        max_blob_size: int,
        blob_storage_bucket: storage.Bucket,
        blob_storage_folder: str,
        tracker: upload_tracker.UploadTracker,
        one_platform_resource_manager: uploader_utils.OnePlatformResourceManager,
    ):
        super().__init__(
            experiment_resource_id,
            api,
            rpc_rate_limiter,
            max_blob_request_size,
            tracker,
            one_platform_resource_manager,
        )
        self._max_blob_size = max_blob_size
        self._bucket = blob_storage_bucket
        self._folder = blob_storage_folder

    def _new_request(self):
        super()._new_request()
        self._blob_sizes = 0

    def _get_tracker(self) -> ContextManager:
        return self._tracker.blob_tracker(0)

    def _create_data_point(
        self,
        run_name: str,
        event: tf.compat.v1.Event,
        value: tf.compat.v1.Summary.Value,
        metadata: tf.compat.v1.SummaryMetadata,
    ) -> tensorboard_data.TimeSeriesDataPoint:
        blobs = tensor_util.make_ndarray(value.tensor)
        if blobs.ndim != 1:
            logger.warning(
                "A blob sequence must be represented as a rank-1 Tensor. "
                "Provided data has rank %d, for run %s, tag %s, step %s ('%s' plugin) .",
                blobs.ndim,
                run_name,
                value.tag,
                event.step,
                metadata.plugin_data.plugin_name,
            )
            return None

        m = re.match(
            ".*/tensorboards/(.*)/experiments/(.*)/runs/(.*)/timeSeries/(.*)",
            self._one_platform_resource_manager.get_time_series_resource_name(
                run_name,
                value.tag,
                lambda: tensorboard_time_series.TensorboardTimeSeries(
                    display_name=value.tag,
                    value_type=tensorboard_time_series.TensorboardTimeSeries.ValueType.BLOB_SEQUENCE,
                    plugin_name=metadata.plugin_data.plugin_name,
                    plugin_data=metadata.plugin_data.content,
                ),
            ),
        )
        blob_path_prefix = "tensorboard-{}/{}/{}/{}".format(m[1], m[2], m[3], m[4])
        blob_path_prefix = (
            "{}/{}".format(self._folder, blob_path_prefix)
            if self._folder
            else blob_path_prefix
        )
        sent_blob_ids = []
        for blob in blobs:
            with self._tracker.blob_tracker(len(blob)) as blob_tracker:
                blob_id = self._send_blob(blob, blob_path_prefix)
                if blob_id is not None:
                    sent_blob_ids.append(str(blob_id))
                    blob_tracker.mark_uploaded(blob_id is not None)

        return tensorboard_data.TimeSeriesDataPoint(
            step=event.step,
            blobs=tensorboard_data.TensorboardBlobSequence(
                values=[
                    tensorboard_data.TensorboardBlob(id=blob_id)
                    for blob_id in sent_blob_ids
                ]
            ),
            wall_time=timestamp.Timestamp(
                seconds=int(event.wall_time),
                nanos=int(round((event.wall_time % 1) * 10**9)),
            ),
        )

    def _send_blob(self, blob, blob_path_prefix):
        """Sends a single blob to a GCS bucket in the consumer project.

        The blob will not be sent if it is too large.

        Returns:
          The ID of blob successfully sent.
        """
        if len(blob) > self._max_blob_size:
            logger.warning(
                "Blob too large; skipping.  Size %d exceeds limit of %d bytes.",
                len(blob),
                self._max_blob_size,
            )
            return None

        blob_id = uuid.uuid4()
        blob_path = (
            "{}/{}".format(blob_path_prefix, blob_id) if blob_path_prefix else blob_id
        )
        self._bucket.blob(blob_path).upload_from_string(blob)
        return blob_id


def _varint_cost(n: int):
    """Computes the size of `n` encoded as an unsigned base-128 varint.

    This should be consistent with the proto wire format:
    <https://developers.google.com/protocol-buffers/docs/encoding#varints>

    Args:
      n: A non-negative integer.

    Returns:
      An integer number of bytes.
    """
    result = 1
    while n >= 128:
        result += 1
        n >>= 7
    return result


def _prune_empty_time_series(
    request: tensorboard_service.WriteTensorboardRunDataRequest,
):
    """Removes empty time_series from request."""
    for (time_series_idx, time_series_data) in reversed(
        list(enumerate(request.time_series_data))
    ):
        if not time_series_data.values:
            del request.time_series_data[time_series_idx]


def _filter_graph_defs(event: tf.compat.v1.Event):
    """Filters graph definitions.

    Args:
      event: tf.compat.v1.Event to filter.
    """
    for v in event.summary.value:
        if v.metadata.plugin_data.plugin_name != graph_metadata.PLUGIN_NAME:
            continue
        if v.tag == graph_metadata.RUN_GRAPH_NAME:
            data = list(v.tensor.string_val)
            filtered_data = [_filtered_graph_bytes(x) for x in data]
            filtered_data = [x for x in filtered_data if x is not None]
            if filtered_data != data:
                new_tensor = tensor_util.make_tensor_proto(
                    filtered_data, dtype=types_pb2.DT_STRING
                )
                v.tensor.CopyFrom(new_tensor)


def _filtered_graph_bytes(graph_bytes: bytes):
    """Prepares the graph to be served to the front-end.

    For now, it supports filtering out attributes that are too large to be shown
    in the graph UI.

    Args:
      graph_bytes: Graph definition.

    Returns:
      Filtered graph.
    """
    try:
        graph_def = graph_pb2.GraphDef().FromString(graph_bytes)
    # The reason for the RuntimeWarning catch here is b/27494216, whereby
    # some proto parsers incorrectly raise that instead of DecodeError
    # on certain kinds of malformed input. Triggering this seems to require
    # a combination of mysterious circumstances.
    except (message.DecodeError, RuntimeWarning):
        logger.warning(
            "Could not parse GraphDef of size %d. Skipping.",
            len(graph_bytes),
        )
        return None
    # Use the default filter parameters:
    # limit_attr_size=1024, large_attrs_key="_too_large_attrs"
    process_graph.prepare_graph_for_ui(graph_def)
    return graph_def.SerializeToString()
