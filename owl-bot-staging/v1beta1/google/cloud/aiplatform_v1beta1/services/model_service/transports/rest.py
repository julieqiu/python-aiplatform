# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.cloud.location import locations_pb2 # type: ignore
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.aiplatform_v1beta1.types import model
from google.cloud.aiplatform_v1beta1.types import model as gca_model
from google.cloud.aiplatform_v1beta1.types import model_evaluation
from google.cloud.aiplatform_v1beta1.types import model_evaluation as gca_model_evaluation
from google.cloud.aiplatform_v1beta1.types import model_evaluation_slice
from google.cloud.aiplatform_v1beta1.types import model_service
from google.longrunning import operations_pb2  # type: ignore

from .base import ModelServiceTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ModelServiceRestInterceptor:
    """Interceptor for ModelService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ModelServiceRestTransport.

    .. code-block:: python
        class MyCustomModelServiceInterceptor(ModelServiceRestInterceptor):
            def pre_batch_import_evaluated_annotations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_import_evaluated_annotations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_import_model_evaluation_slices(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_import_model_evaluation_slices(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_copy_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_copy_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_model_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_model_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model_evaluation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model_evaluation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_model_evaluation_slice(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_model_evaluation_slice(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_model_evaluation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_model_evaluation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_model_evaluations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_model_evaluations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_model_evaluation_slices(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_model_evaluation_slices(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_models(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_models(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_model_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_model_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_merge_version_aliases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_merge_version_aliases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_explanation_dataset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_explanation_dataset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_model(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upload_model(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upload_model(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ModelServiceRestTransport(interceptor=MyCustomModelServiceInterceptor())
        client = ModelServiceClient(transport=transport)


    """
    def pre_batch_import_evaluated_annotations(self, request: model_service.BatchImportEvaluatedAnnotationsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.BatchImportEvaluatedAnnotationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_import_evaluated_annotations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_batch_import_evaluated_annotations(self, response: model_service.BatchImportEvaluatedAnnotationsResponse) -> model_service.BatchImportEvaluatedAnnotationsResponse:
        """Post-rpc interceptor for batch_import_evaluated_annotations

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_batch_import_model_evaluation_slices(self, request: model_service.BatchImportModelEvaluationSlicesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.BatchImportModelEvaluationSlicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_import_model_evaluation_slices

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_batch_import_model_evaluation_slices(self, response: model_service.BatchImportModelEvaluationSlicesResponse) -> model_service.BatchImportModelEvaluationSlicesResponse:
        """Post-rpc interceptor for batch_import_model_evaluation_slices

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_copy_model(self, request: model_service.CopyModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.CopyModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for copy_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_copy_model(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for copy_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_delete_model(self, request: model_service.DeleteModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.DeleteModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_delete_model(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_delete_model_version(self, request: model_service.DeleteModelVersionRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.DeleteModelVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_model_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_delete_model_version(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_model_version

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_export_model(self, request: model_service.ExportModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ExportModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_export_model(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_get_model(self, request: model_service.GetModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.GetModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_model(self, response: model.Model) -> model.Model:
        """Post-rpc interceptor for get_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_get_model_evaluation(self, request: model_service.GetModelEvaluationRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.GetModelEvaluationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model_evaluation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_model_evaluation(self, response: model_evaluation.ModelEvaluation) -> model_evaluation.ModelEvaluation:
        """Post-rpc interceptor for get_model_evaluation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_get_model_evaluation_slice(self, request: model_service.GetModelEvaluationSliceRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.GetModelEvaluationSliceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_model_evaluation_slice

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_model_evaluation_slice(self, response: model_evaluation_slice.ModelEvaluationSlice) -> model_evaluation_slice.ModelEvaluationSlice:
        """Post-rpc interceptor for get_model_evaluation_slice

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_import_model_evaluation(self, request: model_service.ImportModelEvaluationRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ImportModelEvaluationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_model_evaluation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_import_model_evaluation(self, response: gca_model_evaluation.ModelEvaluation) -> gca_model_evaluation.ModelEvaluation:
        """Post-rpc interceptor for import_model_evaluation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_model_evaluations(self, request: model_service.ListModelEvaluationsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ListModelEvaluationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_model_evaluations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_model_evaluations(self, response: model_service.ListModelEvaluationsResponse) -> model_service.ListModelEvaluationsResponse:
        """Post-rpc interceptor for list_model_evaluations

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_model_evaluation_slices(self, request: model_service.ListModelEvaluationSlicesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ListModelEvaluationSlicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_model_evaluation_slices

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_model_evaluation_slices(self, response: model_service.ListModelEvaluationSlicesResponse) -> model_service.ListModelEvaluationSlicesResponse:
        """Post-rpc interceptor for list_model_evaluation_slices

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_models(self, request: model_service.ListModelsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ListModelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_models

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_models(self, response: model_service.ListModelsResponse) -> model_service.ListModelsResponse:
        """Post-rpc interceptor for list_models

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_model_versions(self, request: model_service.ListModelVersionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.ListModelVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_model_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_model_versions(self, response: model_service.ListModelVersionsResponse) -> model_service.ListModelVersionsResponse:
        """Post-rpc interceptor for list_model_versions

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_merge_version_aliases(self, request: model_service.MergeVersionAliasesRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.MergeVersionAliasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for merge_version_aliases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_merge_version_aliases(self, response: model.Model) -> model.Model:
        """Post-rpc interceptor for merge_version_aliases

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_update_explanation_dataset(self, request: model_service.UpdateExplanationDatasetRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.UpdateExplanationDatasetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_explanation_dataset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_update_explanation_dataset(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_explanation_dataset

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_update_model(self, request: model_service.UpdateModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.UpdateModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_update_model(self, response: gca_model.Model) -> gca_model.Model:
        """Post-rpc interceptor for update_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_upload_model(self, request: model_service.UploadModelRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[model_service.UploadModelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for upload_model

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_upload_model(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for upload_model

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self, request: locations_pb2.GetLocationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_locations(
        self, request: locations_pb2.ListLocationsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_get_iam_policy(
        self, request: iam_policy_pb2.GetIamPolicyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_iam_policy(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_set_iam_policy(
        self, request: iam_policy_pb2.SetIamPolicyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_set_iam_policy(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_test_iam_permissions(
        self, request: iam_policy_pb2.TestIamPermissionsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_cancel_operation(
        self, request: operations_pb2.CancelOperationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_cancel_operation(
        self, response: None
    ) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_delete_operation(
        self, request: operations_pb2.DeleteOperationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_delete_operation(
        self, response: None
    ) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_get_operation(
        self, request: operations_pb2.GetOperationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_list_operations(
        self, request: operations_pb2.ListOperationsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response
    def pre_wait_operation(
        self, request: operations_pb2.WaitOperationRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[operations_pb2.WaitOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for wait_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ModelService server.
        """
        return request, metadata

    def post_wait_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for wait_operation

        Override in a subclass to manipulate the response
        after it is returned by the ModelService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ModelServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ModelServiceRestInterceptor


class ModelServiceRestTransport(ModelServiceTransport):
    """REST backend transport for ModelService.

    A service for managing Vertex AI's machine learning Models.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(self, *,
            host: str = 'aiplatform.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[ModelServiceRestInterceptor] = None,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

       NOTE: This REST transport functionality is currently in a beta
       state (preview). We welcome your feedback via a GitHub issue in
       this library's repository. Thank you!

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'aiplatform.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ModelServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                'google.longrunning.Operations.CancelOperation': [
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:cancel',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:cancel',
                    },
                ],
                'google.longrunning.Operations.DeleteOperation': [
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*}/operations',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/extensions/*}/operations',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
                    },
                    {
                        'method': 'delete',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
                    },
                ],
                'google.longrunning.Operations.GetOperation': [
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDeploymentJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
                    },
                ],
                'google.longrunning.Operations.ListOperations': [
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/endpoints/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/extensions/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/customJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/indexes/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/migratableResources/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/models/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/schedules/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/specialistPools/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*}/operations',
                    },
                    {
                        'method': 'get',
                        'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*}/operations',
                    },
                ],
                'google.longrunning.Operations.WaitOperation': [
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
                    },
                    {
                        'method': 'post',
                        'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                    host=self._host,
                    # use the credentials which are saved
                    credentials=self._credentials,
                    scopes=self._scopes,
                    http_options=http_options,
                    path_prefix="v1beta1")

            self._operations_client = operations_v1.AbstractOperationsClient(transport=rest_transport)

        # Return the client from cache.
        return self._operations_client

    class _BatchImportEvaluatedAnnotations(ModelServiceRestStub):
        def __hash__(self):
            return hash("BatchImportEvaluatedAnnotations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.BatchImportEvaluatedAnnotationsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.BatchImportEvaluatedAnnotationsResponse:
            r"""Call the batch import evaluated
        annotations method over HTTP.

            Args:
                request (~.model_service.BatchImportEvaluatedAnnotationsRequest):
                    The request object. Request message for
                [ModelService.BatchImportEvaluatedAnnotations][google.cloud.aiplatform.v1beta1.ModelService.BatchImportEvaluatedAnnotations]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.BatchImportEvaluatedAnnotationsResponse:
                    Response message for
                [ModelService.BatchImportEvaluatedAnnotations][google.cloud.aiplatform.v1beta1.ModelService.BatchImportEvaluatedAnnotations]

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{parent=projects/*/locations/*/models/*/evaluations/*/slices/*}:batchImport',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_import_evaluated_annotations(request, metadata)
            pb_request = model_service.BatchImportEvaluatedAnnotationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.BatchImportEvaluatedAnnotationsResponse()
            pb_resp = model_service.BatchImportEvaluatedAnnotationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_import_evaluated_annotations(resp)
            return resp

    class _BatchImportModelEvaluationSlices(ModelServiceRestStub):
        def __hash__(self):
            return hash("BatchImportModelEvaluationSlices")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.BatchImportModelEvaluationSlicesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.BatchImportModelEvaluationSlicesResponse:
            r"""Call the batch import model
        evaluation slices method over HTTP.

            Args:
                request (~.model_service.BatchImportModelEvaluationSlicesRequest):
                    The request object. Request message for
                [ModelService.BatchImportModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.BatchImportModelEvaluationSlices]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.BatchImportModelEvaluationSlicesResponse:
                    Response message for
                [ModelService.BatchImportModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.BatchImportModelEvaluationSlices]

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{parent=projects/*/locations/*/models/*/evaluations/*}/slices:batchImport',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_import_model_evaluation_slices(request, metadata)
            pb_request = model_service.BatchImportModelEvaluationSlicesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.BatchImportModelEvaluationSlicesResponse()
            pb_resp = model_service.BatchImportModelEvaluationSlicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_import_model_evaluation_slices(resp)
            return resp

    class _CopyModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("CopyModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.CopyModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the copy model method over HTTP.

            Args:
                request (~.model_service.CopyModelRequest):
                    The request object. Request message for
                [ModelService.CopyModel][google.cloud.aiplatform.v1beta1.ModelService.CopyModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{parent=projects/*/locations/*}/models:copy',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_copy_model(request, metadata)
            pb_request = model_service.CopyModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_copy_model(resp)
            return resp

    class _DeleteModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("DeleteModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.DeleteModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the delete model method over HTTP.

            Args:
                request (~.model_service.DeleteModelRequest):
                    The request object. Request message for
                [ModelService.DeleteModel][google.cloud.aiplatform.v1beta1.ModelService.DeleteModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_model(request, metadata)
            pb_request = model_service.DeleteModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_model(resp)
            return resp

    class _DeleteModelVersion(ModelServiceRestStub):
        def __hash__(self):
            return hash("DeleteModelVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.DeleteModelVersionRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the delete model version method over HTTP.

            Args:
                request (~.model_service.DeleteModelVersionRequest):
                    The request object. Request message for
                [ModelService.DeleteModelVersion][google.cloud.aiplatform.v1beta1.ModelService.DeleteModelVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}:deleteVersion',
            },
            ]
            request, metadata = self._interceptor.pre_delete_model_version(request, metadata)
            pb_request = model_service.DeleteModelVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_model_version(resp)
            return resp

    class _ExportModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("ExportModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ExportModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the export model method over HTTP.

            Args:
                request (~.model_service.ExportModelRequest):
                    The request object. Request message for
                [ModelService.ExportModel][google.cloud.aiplatform.v1beta1.ModelService.ExportModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}:export',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_export_model(request, metadata)
            pb_request = model_service.ExportModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_model(resp)
            return resp

    class _GetModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("GetModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.GetModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model.Model:
            r"""Call the get model method over HTTP.

            Args:
                request (~.model_service.GetModelRequest):
                    The request object. Request message for
                [ModelService.GetModel][google.cloud.aiplatform.v1beta1.ModelService.GetModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model.Model:
                    A trained machine learning Model.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_model(request, metadata)
            pb_request = model_service.GetModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model.Model()
            pb_resp = model.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model(resp)
            return resp

    class _GetModelEvaluation(ModelServiceRestStub):
        def __hash__(self):
            return hash("GetModelEvaluation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.GetModelEvaluationRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_evaluation.ModelEvaluation:
            r"""Call the get model evaluation method over HTTP.

            Args:
                request (~.model_service.GetModelEvaluationRequest):
                    The request object. Request message for
                [ModelService.GetModelEvaluation][google.cloud.aiplatform.v1beta1.ModelService.GetModelEvaluation].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_evaluation.ModelEvaluation:
                    A collection of metrics calculated by
                comparing Model's predictions on all of
                the test data against annotations from
                the test data.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_model_evaluation(request, metadata)
            pb_request = model_service.GetModelEvaluationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_evaluation.ModelEvaluation()
            pb_resp = model_evaluation.ModelEvaluation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model_evaluation(resp)
            return resp

    class _GetModelEvaluationSlice(ModelServiceRestStub):
        def __hash__(self):
            return hash("GetModelEvaluationSlice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.GetModelEvaluationSliceRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_evaluation_slice.ModelEvaluationSlice:
            r"""Call the get model evaluation
        slice method over HTTP.

            Args:
                request (~.model_service.GetModelEvaluationSliceRequest):
                    The request object. Request message for
                [ModelService.GetModelEvaluationSlice][google.cloud.aiplatform.v1beta1.ModelService.GetModelEvaluationSlice].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_evaluation_slice.ModelEvaluationSlice:
                    A collection of metrics calculated by
                comparing Model's predictions on a slice
                of the test data against ground truth
                annotations.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/slices/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_model_evaluation_slice(request, metadata)
            pb_request = model_service.GetModelEvaluationSliceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_evaluation_slice.ModelEvaluationSlice()
            pb_resp = model_evaluation_slice.ModelEvaluationSlice.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_model_evaluation_slice(resp)
            return resp

    class _ImportModelEvaluation(ModelServiceRestStub):
        def __hash__(self):
            return hash("ImportModelEvaluation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ImportModelEvaluationRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> gca_model_evaluation.ModelEvaluation:
            r"""Call the import model evaluation method over HTTP.

            Args:
                request (~.model_service.ImportModelEvaluationRequest):
                    The request object. Request message for
                [ModelService.ImportModelEvaluation][google.cloud.aiplatform.v1beta1.ModelService.ImportModelEvaluation]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gca_model_evaluation.ModelEvaluation:
                    A collection of metrics calculated by
                comparing Model's predictions on all of
                the test data against annotations from
                the test data.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{parent=projects/*/locations/*/models/*}/evaluations:import',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_import_model_evaluation(request, metadata)
            pb_request = model_service.ImportModelEvaluationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gca_model_evaluation.ModelEvaluation()
            pb_resp = gca_model_evaluation.ModelEvaluation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_model_evaluation(resp)
            return resp

    class _ListModelEvaluations(ModelServiceRestStub):
        def __hash__(self):
            return hash("ListModelEvaluations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ListModelEvaluationsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.ListModelEvaluationsResponse:
            r"""Call the list model evaluations method over HTTP.

            Args:
                request (~.model_service.ListModelEvaluationsRequest):
                    The request object. Request message for
                [ModelService.ListModelEvaluations][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluations].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.ListModelEvaluationsResponse:
                    Response message for
                [ModelService.ListModelEvaluations][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluations].

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{parent=projects/*/locations/*/models/*}/evaluations',
            },
            ]
            request, metadata = self._interceptor.pre_list_model_evaluations(request, metadata)
            pb_request = model_service.ListModelEvaluationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.ListModelEvaluationsResponse()
            pb_resp = model_service.ListModelEvaluationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_model_evaluations(resp)
            return resp

    class _ListModelEvaluationSlices(ModelServiceRestStub):
        def __hash__(self):
            return hash("ListModelEvaluationSlices")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ListModelEvaluationSlicesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.ListModelEvaluationSlicesResponse:
            r"""Call the list model evaluation
        slices method over HTTP.

            Args:
                request (~.model_service.ListModelEvaluationSlicesRequest):
                    The request object. Request message for
                [ModelService.ListModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluationSlices].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.ListModelEvaluationSlicesResponse:
                    Response message for
                [ModelService.ListModelEvaluationSlices][google.cloud.aiplatform.v1beta1.ModelService.ListModelEvaluationSlices].

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{parent=projects/*/locations/*/models/*/evaluations/*}/slices',
            },
            ]
            request, metadata = self._interceptor.pre_list_model_evaluation_slices(request, metadata)
            pb_request = model_service.ListModelEvaluationSlicesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.ListModelEvaluationSlicesResponse()
            pb_resp = model_service.ListModelEvaluationSlicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_model_evaluation_slices(resp)
            return resp

    class _ListModels(ModelServiceRestStub):
        def __hash__(self):
            return hash("ListModels")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ListModelsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.ListModelsResponse:
            r"""Call the list models method over HTTP.

            Args:
                request (~.model_service.ListModelsRequest):
                    The request object. Request message for
                [ModelService.ListModels][google.cloud.aiplatform.v1beta1.ModelService.ListModels].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.ListModelsResponse:
                    Response message for
                [ModelService.ListModels][google.cloud.aiplatform.v1beta1.ModelService.ListModels]

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{parent=projects/*/locations/*}/models',
            },
            ]
            request, metadata = self._interceptor.pre_list_models(request, metadata)
            pb_request = model_service.ListModelsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.ListModelsResponse()
            pb_resp = model_service.ListModelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_models(resp)
            return resp

    class _ListModelVersions(ModelServiceRestStub):
        def __hash__(self):
            return hash("ListModelVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.ListModelVersionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model_service.ListModelVersionsResponse:
            r"""Call the list model versions method over HTTP.

            Args:
                request (~.model_service.ListModelVersionsRequest):
                    The request object. Request message for
                [ModelService.ListModelVersions][google.cloud.aiplatform.v1beta1.ModelService.ListModelVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model_service.ListModelVersionsResponse:
                    Response message for
                [ModelService.ListModelVersions][google.cloud.aiplatform.v1beta1.ModelService.ListModelVersions]

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}:listVersions',
            },
            ]
            request, metadata = self._interceptor.pre_list_model_versions(request, metadata)
            pb_request = model_service.ListModelVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model_service.ListModelVersionsResponse()
            pb_resp = model_service.ListModelVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_model_versions(resp)
            return resp

    class _MergeVersionAliases(ModelServiceRestStub):
        def __hash__(self):
            return hash("MergeVersionAliases")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.MergeVersionAliasesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> model.Model:
            r"""Call the merge version aliases method over HTTP.

            Args:
                request (~.model_service.MergeVersionAliasesRequest):
                    The request object. Request message for
                [ModelService.MergeVersionAliases][google.cloud.aiplatform.v1beta1.ModelService.MergeVersionAliases].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.model.Model:
                    A trained machine learning Model.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}:mergeVersionAliases',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_merge_version_aliases(request, metadata)
            pb_request = model_service.MergeVersionAliasesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = model.Model()
            pb_resp = model.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_merge_version_aliases(resp)
            return resp

    class _UpdateExplanationDataset(ModelServiceRestStub):
        def __hash__(self):
            return hash("UpdateExplanationDataset")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.UpdateExplanationDatasetRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the update explanation
        dataset method over HTTP.

            Args:
                request (~.model_service.UpdateExplanationDatasetRequest):
                    The request object. Request message for
                [ModelService.UpdateExplanationDataset][google.cloud.aiplatform.v1beta1.ModelService.UpdateExplanationDataset].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{model=projects/*/locations/*/models/*}:updateExplanationDataset',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_update_explanation_dataset(request, metadata)
            pb_request = model_service.UpdateExplanationDatasetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_explanation_dataset(resp)
            return resp

    class _UpdateModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("UpdateModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "updateMask" : {},        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.UpdateModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> gca_model.Model:
            r"""Call the update model method over HTTP.

            Args:
                request (~.model_service.UpdateModelRequest):
                    The request object. Request message for
                [ModelService.UpdateModel][google.cloud.aiplatform.v1beta1.ModelService.UpdateModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gca_model.Model:
                    A trained machine learning Model.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v1beta1/{model.name=projects/*/locations/*/models/*}',
                'body': 'model',
            },
            ]
            request, metadata = self._interceptor.pre_update_model(request, metadata)
            pb_request = model_service.UpdateModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gca_model.Model()
            pb_resp = gca_model.Model.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_model(resp)
            return resp

    class _UploadModel(ModelServiceRestStub):
        def __hash__(self):
            return hash("UploadModel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: model_service.UploadModelRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the upload model method over HTTP.

            Args:
                request (~.model_service.UploadModelRequest):
                    The request object. Request message for
                [ModelService.UploadModel][google.cloud.aiplatform.v1beta1.ModelService.UploadModel].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{parent=projects/*/locations/*}/models:upload',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_upload_model(request, metadata)
            pb_request = model_service.UploadModelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_upload_model(resp)
            return resp

    @property
    def batch_import_evaluated_annotations(self) -> Callable[
            [model_service.BatchImportEvaluatedAnnotationsRequest],
            model_service.BatchImportEvaluatedAnnotationsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchImportEvaluatedAnnotations(self._session, self._host, self._interceptor) # type: ignore

    @property
    def batch_import_model_evaluation_slices(self) -> Callable[
            [model_service.BatchImportModelEvaluationSlicesRequest],
            model_service.BatchImportModelEvaluationSlicesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchImportModelEvaluationSlices(self._session, self._host, self._interceptor) # type: ignore

    @property
    def copy_model(self) -> Callable[
            [model_service.CopyModelRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CopyModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_model(self) -> Callable[
            [model_service.DeleteModelRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_model_version(self) -> Callable[
            [model_service.DeleteModelVersionRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteModelVersion(self._session, self._host, self._interceptor) # type: ignore

    @property
    def export_model(self) -> Callable[
            [model_service.ExportModelRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_model(self) -> Callable[
            [model_service.GetModelRequest],
            model.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_model_evaluation(self) -> Callable[
            [model_service.GetModelEvaluationRequest],
            model_evaluation.ModelEvaluation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModelEvaluation(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_model_evaluation_slice(self) -> Callable[
            [model_service.GetModelEvaluationSliceRequest],
            model_evaluation_slice.ModelEvaluationSlice]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetModelEvaluationSlice(self._session, self._host, self._interceptor) # type: ignore

    @property
    def import_model_evaluation(self) -> Callable[
            [model_service.ImportModelEvaluationRequest],
            gca_model_evaluation.ModelEvaluation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportModelEvaluation(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_model_evaluations(self) -> Callable[
            [model_service.ListModelEvaluationsRequest],
            model_service.ListModelEvaluationsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModelEvaluations(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_model_evaluation_slices(self) -> Callable[
            [model_service.ListModelEvaluationSlicesRequest],
            model_service.ListModelEvaluationSlicesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModelEvaluationSlices(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_models(self) -> Callable[
            [model_service.ListModelsRequest],
            model_service.ListModelsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModels(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_model_versions(self) -> Callable[
            [model_service.ListModelVersionsRequest],
            model_service.ListModelVersionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListModelVersions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def merge_version_aliases(self) -> Callable[
            [model_service.MergeVersionAliasesRequest],
            model.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MergeVersionAliases(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_explanation_dataset(self) -> Callable[
            [model_service.UpdateExplanationDatasetRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExplanationDataset(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_model(self) -> Callable[
            [model_service.UpdateModelRequest],
            gca_model.Model]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def upload_model(self) -> Callable[
            [model_service.UploadModelRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UploadModel(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor) # type: ignore

    class _GetLocation(ModelServiceRestStub):
        def __call__(self,
            request: locations_pb2.GetLocationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> locations_pb2.Location:

            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*}',
            },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor) # type: ignore

    class _ListLocations(ModelServiceRestStub):
        def __call__(self,
            request: locations_pb2.ListLocationsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> locations_pb2.ListLocationsResponse:

            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/ui/{name=projects/*}/locations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*}/locations',
            },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor) # type: ignore

    class _GetIamPolicy(ModelServiceRestStub):
        def __call__(self,
            request: iam_policy_pb2.GetIamPolicyRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> policy_pb2.Policy:

            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*}:getIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/models/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/endpoints/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/publishers/*/models/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/models/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/endpoints/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/publishers/*/models/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*}:getIamPolicy',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:getIamPolicy',
            },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            body = json.dumps(transcoded_request['body'])
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor) # type: ignore

    class _SetIamPolicy(ModelServiceRestStub):
        def __call__(self,
            request: iam_policy_pb2.SetIamPolicyRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> policy_pb2.Policy:

            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/models/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/endpoints/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/models/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/endpoints/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*}:setIamPolicy',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:setIamPolicy',
                'body': '*',
            },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            body = json.dumps(transcoded_request['body'])
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor) # type: ignore

    class _TestIamPermissions(ModelServiceRestStub):
        def __call__(self,
            request: iam_policy_pb2.TestIamPermissionsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> iam_policy_pb2.TestIamPermissionsResponse:

            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*}:testIamPermissions',
                'body': '*',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/models/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/endpoints/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featurestores/*/entityTypes/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/models/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/endpoints/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/notebookRuntimeTemplates/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*}:testIamPermissions',
            },
{
                'method': 'post',
                'uri': '/ui/{resource=projects/*/locations/*/featureOnlineStores/*/featureViews/*}:testIamPermissions',
            },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            body = json.dumps(transcoded_request['body'])
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor) # type: ignore

    class _CancelOperation(ModelServiceRestStub):
        def __call__(self,
            request: operations_pb2.CancelOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> None:

            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:cancel',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:cancel',
            },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor) # type: ignore

    class _DeleteOperation(ModelServiceRestStub):
        def __call__(self,
            request: operations_pb2.DeleteOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> None:

            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*}/operations',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/extensions/*}/operations',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
            },
{
                'method': 'delete',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
            },
            ]

            request, metadata = self._interceptor.pre_delete_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor) # type: ignore

    class _GetOperation(ModelServiceRestStub):
        def __call__(self,
            request: operations_pb2.GetOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> operations_pb2.Operation:

            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/edgeDeploymentJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}',
            },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor) # type: ignore

    class _ListOperations(ModelServiceRestStub):
        def __call__(self,
            request: operations_pb2.ListOperationsRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> operations_pb2.ListOperationsResponse:

            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/endpoints/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/extensions/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/customJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/indexes/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/migratableResources/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/models/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/studies/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/schedules/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/specialistPools/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/solvers/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*}/operations',
            },
{
                'method': 'get',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*}/operations',
            },
{
                'method': 'get',
                'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*}/operations',
            },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def wait_operation(self):
        return self._WaitOperation(self._session, self._host, self._interceptor) # type: ignore

    class _WaitOperation(ModelServiceRestStub):
        def __call__(self,
            request: operations_pb2.WaitOperationRequest, *,
            retry: OptionalRetry=gapic_v1.method.DEFAULT,
            timeout: Optional[float]=None,
            metadata: Sequence[Tuple[str, str]]=(),
            ) -> operations_pb2.Operation:

            r"""Call the wait operation method over HTTP.

            Args:
                request (operations_pb2.WaitOperationRequest):
                    The request object for WaitOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from WaitOperation method.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/edgeDevices/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/endpoints/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/extensionControllers/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/extensions/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/customJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tuningJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/indexes/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/modelMonitors/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/migratableResources/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/models/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/schedules/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/specialistPools/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/ui/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/savedQueries/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/annotationSpecs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/datasets/*/dataItems/*/annotations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/deploymentResourcePools/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/edgeDevices/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/endpoints/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/evaluationTasks/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/exampleStores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensionControllers/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/extensions/*/deployments/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featurestores/*/entityTypes/*/features/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/customJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/dataLabelingJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/hyperparameterTuningJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexes/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/indexEndpoints/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/artifacts/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/contexts/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/metadataStores/*/executions/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelDeploymentMonitoringJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/modelMonitors/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/migratableResources/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/models/*/evaluations/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/persistentResources/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/ragCorpora/*/ragFiles/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/reasoningEngines/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/studies/*/trials/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/trainingPipelines/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/pipelineJobs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/schedules/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/specialistPools/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureOnlineStores/*/featureViews/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/operations/*}:wait',
            },
{
                'method': 'post',
                'uri': '/v1beta1/{name=projects/*/locations/*/featureGroups/*/features/*/operations/*}:wait',
            },
            ]

            request, metadata = self._interceptor.pre_wait_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request['query_params']))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_wait_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'ModelServiceRestTransport',
)
