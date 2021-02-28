"""Datatype definition."""

from typing import Dict, List, Union, Any


class DsTarget:
    """Datastructure for target."""

    @property
    def name(self) -> str:
        """Display name."""
        return self.__name

    @property
    def groups(self) -> Dict[str, str]:
        """Custom groups of a target. E.g.: env, page, type..."""
        return self.__groups

    @property
    def url(self) -> str:
        """Url of the target."""
        return self.__url

    @property
    def method(self) -> str:
        """Request method."""
        return self.__method

    @property
    def params(self) -> Dict[str, str]:
        """Additional parameters to parse to the request."""
        return self.__params

    @property
    def headers(self) -> Dict[str, str]:
        """Additional headers to parse to the request."""
        return self.__headers

    @property
    def timeout(self) -> Union[int, float]:
        """Timeout to wait for the request to finish."""
        return self.__timeout

    @property
    def basic_auth(self) -> Dict[str, str]:
        """Basic auth data."""
        return self.__basic_auth

    @property
    def digest_auth(self) -> Dict[str, str]:
        """Digest auth data."""
        return self.__digest_auth

    @property
    def fail_if(self) -> Dict[str, Any]:
        """Fail if conditions."""
        return self.__fail_if

    @property
    def extract(self) -> Dict[str, List[str]]:
        """Extract regexes."""
        return self.__extract

    def __init__(self, target: Dict[str, Any]) -> None:
        self.__name = str(target["name"])
        self.__groups = dict(target["groups"])
        self.__url = str(target["url"])
        self.__method = str(target["method"])
        self.__params = dict(target["params"])
        self.__headers = dict(target["headers"])
        self.__timeout = float(target["timeout"])
        self.__basic_auth = dict(target["basic_auth"])
        self.__digest_auth = dict(target["digest_auth"])
        self.__fail_if = dict(target["fail_if"])
        self.__extract = dict(target["extract"])
