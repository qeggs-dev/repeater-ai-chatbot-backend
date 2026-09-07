from .request_logs_types import RequestLogTypes
from typing import Any
from pydantic import BaseModel

class ValidateRequestLog(BaseModel):
    request_log_type: RequestLogTypes

def validate_request_log(request_log_type: Any) -> RequestLogTypes:
    """
    Validate the request log type.

    Args:
        request_log_type (RequestLogTypes): The request log type.

    Returns:
        RequestLogTypes: The validated request log type.
    """
    model = ValidateRequestLog(
        request_log_type = request_log_type
    )

    return model.request_log_type
