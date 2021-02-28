"""Datatype definition."""

from typing import Dict, List, Any


class DsResponse:
    """Datastructure for response."""

    @property
    def name(self) -> str:
        """Unique name of this response."""
        return self.__name

    @property
    def groups(self) -> Dict[str, str]:
        """Additional specified groups."""
        return self.__groups

    @property
    def url(self) -> str:
        """Request URL."""
        return self.__url

    @property
    def headers(self) -> Dict[str, str]:
        """Response headers."""
        return self.__headers

    @property
    def body(self) -> bytes:
        """Response body."""
        return self.__body

    @property
    def size(self) -> int:
        """Response body size in bytes."""
        return self.__size

    @property
    def time_ttfb(self) -> float:
        """Time to first byte."""
        return self.__time_ttfb

    @property
    def time_download(self) -> float:
        """Time taken to download response."""
        return self.__time_download

    @property
    def time_render(self) -> float:
        """Time taken to render the document."""
        return self.__time_render

    @property
    def time_total(self) -> float:
        """Total time taken."""
        return self.__time_total

    @property
    def status_code(self) -> int:
        """HTTP status code returned from server."""
        return self.__status_code

    @property
    def status_family(self) -> str:
        """HTTP status code family returned from server (e.g.: '4xx')."""
        return self.__status_family

    @property
    def success(self) -> bool:
        """Returns True if request was successful."""
        return self.__success

    @success.setter
    def success(self, value: bool) -> None:
        self.__success = value

    @property
    def err_msg(self) -> str:
        """Contains the error message in case the request was not successful."""
        return self.__err_msg

    @err_msg.setter
    def err_msg(self, value: str) -> None:
        self.__err_msg = value

    @property
    def extract(self) -> List[str]:
        """Contains a list of regex extracted string from the body."""
        return self.__extract

    def __init__(self, response: Dict[str, Any]) -> None:
        self.__name = str(response["name"])
        self.__groups = dict(response["groups"])
        self.__url = str(response["url"])
        self.__headers = dict(response["headers"])
        self.__body = bytes(response["body"])
        self.__size = int(response["size"])
        self.__time_ttfb = float(response["time_ttfb"])
        self.__time_download = float(response["time_download"])
        self.__time_render = float(response["time_render"])
        self.__time_total = float(response["time_total"])
        self.__status_code = int(response["status_code"])
        self.__status_family = str(response["status_family"])
        self.__success = bool(response["success"])
        self.__err_msg = str(response["err_msg"])
        self.__extract = list(response["extract"])
