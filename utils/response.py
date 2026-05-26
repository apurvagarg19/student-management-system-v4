from typing import Any, Optional


def success_response(
    data: Optional[Any] = None,
    message: str = "Success"
):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    message: str = "Error",
    data: Optional[Any] = None
):

    return {
        "success": False,
        "message": message,
        "data": data
    }