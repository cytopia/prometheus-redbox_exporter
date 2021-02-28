"""Abstract class definition."""

from typing import List, Dict

import re
from abc import ABC
from abc import abstractmethod

from ..types import DsTarget
from ..types import DsResponse
from ..conditions import evaluate_response


class Request(ABC):
    """Abstract class to be implemented by all Request handlers."""

    # --------------------------------------------------------------------------
    # Abstract Functions
    # --------------------------------------------------------------------------
    @abstractmethod
    def request(self, target: DsTarget) -> DsResponse:
        """Make a request and return the response."""
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    @staticmethod
    def build_valid_response(
        target: DsTarget,
        headers: Dict[str, str],
        body: bytes,
        time_ttfb: float,
        time_download: float,
        time_render: float,
        status_code: int,
    ) -> DsResponse:
        """Get a filled in data structure for a succeeded response."""
        return evaluate_response(
            target,
            DsResponse(
                {
                    "name": target.name,
                    "groups": target.groups,
                    "url": target.url,
                    "headers": headers,
                    "body": body,
                    "size": len(body),
                    "time_ttfb": time_ttfb,
                    "time_download": time_download,
                    "time_render": time_render,
                    "time_total": (time_ttfb + time_download + time_render),
                    "status_code": status_code,
                    "status_family": str(status_code)[0] + "xx",
                    "success": True,
                    "extract": Request.__extract_from_body(target, body, status_code),
                    "err_msg": "",
                }
            ),
        )

    @staticmethod
    def build_failed_response(target: DsTarget, err_msg: str) -> DsResponse:
        """Get a filled in data structure for a failed response."""
        return DsResponse(
            {
                "name": target.name,
                "groups": target.groups,
                "url": target.url,
                "headers": [],
                "body": b"",
                "size": 0,
                "time_ttfb": 0,
                "time_download": 0,
                "time_render": 0,
                "time_total": 0,
                "status_code": 0,
                "status_family": "0xx",
                "success": False,
                "extract": [],
                "err_msg": err_msg,
            }
        )

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    @staticmethod
    def __extract_from_body(target: DsTarget, body: bytes, status_code: int) -> List[str]:
        """Create human readable error message."""
        if target.extract:
            if str(status_code) in target.extract:
                for regex in target.extract[str(status_code)]:
                    regobj = re.compile(regex.encode(), re.IGNORECASE)
                    result = regobj.findall(body)
                    if result:
                        return [item.decode("utf-8") for item in result]

            if str(status_code)[0] + "xx" in target.extract:
                for regex in target.extract[str(status_code)[0] + "xx"]:
                    regobj = re.compile(regex.encode(), re.IGNORECASE)
                    result = regobj.findall(body)
                    if result:
                        return [item.decode("utf-8") for item in result]

            if "*" in target.extract:
                for regex in target.extract["*"]:
                    regobj = re.compile(regex.encode(), re.IGNORECASE)
                    result = regobj.findall(body)
                    if result:
                        return [item.decode("utf-8") for item in result]
        return []
