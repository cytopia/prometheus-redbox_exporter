"""Evaluate response based on conditions."""

from typing import Dict, Any

from .types import DsTarget
from .types import DsResponse


# -------------------------------------------------------------------------------------------------
# Public Methods
# -------------------------------------------------------------------------------------------------
def evaluate_response(target: DsTarget, response: DsResponse) -> DsResponse:
    """Evaluate response based on defined config ressings."""
    # If it had already failed, we do not need to evaluate further
    if not response.success:
        return response

    # If we do not have any conditions defined, return as it is
    if not target.fail_if:
        return response

    # Evaluate
    response = __status_code_not_in(response, target.fail_if)
    return response


# -------------------------------------------------------------------------------------------------
# Hidden Methods
# -------------------------------------------------------------------------------------------------
def __status_code_not_in(response: DsResponse, fail_if: Dict[str, Any]) -> DsResponse:
    """Evaluate status_code_not_in."""
    # Check status_code
    if "status_code_not_in" in fail_if:
        if fail_if["status_code_not_in"]:
            status_code = response.status_code
            status_list = [int(i) for i in fail_if["status_code_not_in"]]
            if status_code not in status_list:
                response.success = False
                response.err_msg = "Condition Error: Http status code {} not in: {}".format(
                    str(status_code), ",".join([str(i) for i in fail_if["status_code_not_in"]])
                )
    return response
