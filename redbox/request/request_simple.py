"""Make HTTP requests to defined targets."""

from typing import Optional, Any, Tuple, Union

import re
import sys
import timeit

import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

from .types import DsResponse
from .types import DsTarget
from .classes import Request


class RequestSimple(Request):
    """Simple HTTP request."""

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def request(self, target: DsTarget) -> DsResponse:
        """Make Http request and return response."""
        error = ""
        failed = 0
        request_time = float(0)
        try:
            auth = RequestSimple.__get_auth(target)
            timeout = RequestSimple.__get_timeout(target)

            start = timeit.default_timer()
            response = requests.request(
                target.method,
                target.url,
                params=target.params,
                headers=target.headers,
                timeout=timeout,
                auth=auth,
            )
            # Note: response.elapsed.total_seconds() will only get you the time it takes
            # until you get the return headers without the response contents.
            # So here we also measure the complete request time including the body response.
            request_time = timeit.default_timer() - start

        except requests.exceptions.URLRequired as url_err:
            error = str(url_err)
            failed = 1
        except requests.exceptions.HTTPError as http_err:
            error = str(http_err)
            failed = 1
        except requests.exceptions.TooManyRedirects as redir_err:
            error = str(redir_err)
            failed = 1
        except requests.exceptions.ConnectTimeout as conn_time_err:
            error = str(conn_time_err)
            failed = 1
        except requests.exceptions.ReadTimeout as read_time_err:
            error = str(read_time_err)
            failed = 1
        except requests.exceptions.Timeout as time_err:
            error = str(time_err)
            failed = 1
        except requests.exceptions.ConnectionError as conn_err:
            error = str(conn_err)
            failed = 1
        except requests.exceptions.RequestException as req_err:
            error = str(req_err)
            failed = 1
        else:
            response.close()

        print(
            "Target Response [{}]: {} sec for {}".format(
                0 if failed else response.status_code, "{0:.3f}".format(request_time), target.name
            ),
            file=sys.stderr,
        )

        if failed == 1:
            return self.build_failed_response(target, RequestSimple.__format_error(error))

        return self.build_valid_response(
            target,
            dict(response.headers),
            response.content,
            response.elapsed.total_seconds(),
            request_time - response.elapsed.total_seconds(),
            float(0),
            response.status_code,
        )

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    @staticmethod
    def __format_error(error: str) -> str:
        """Create human readable error message."""
        regex = re.compile("(.*object at 0x[A-Fa-f0-9]+>[,:])(.*)")
        match = regex.match(error)
        if match:
            try:
                human = match.group(len(match.groups()))
                human = human.strip()
                human = human.rstrip("'))")
                return human
            except AttributeError:
                pass
        return str(error)

    @staticmethod
    def __get_auth(target: DsTarget) -> Optional[Any]:
        """Get authentication mechanism if defined."""
        if target.basic_auth:
            return HTTPBasicAuth(
                target.basic_auth["username"],
                target.basic_auth["password"],
            )
        if target.digest_auth:
            return HTTPDigestAuth(
                target.digest_auth["username"],
                target.digest_auth["password"],
            )
        return None

    @staticmethod
    def __get_timeout(target: DsTarget) -> Tuple[Union[int, float], Union[int, float]]:
        """Get timeout values."""
        # The connect timeout is the number of seconds Requests will wait for your client to
        # establish a connection to a remote machine (corresponding to the connect()) call on
        # the socket. It’s a good practice to set connect timeouts to slightly larger than a
        # multiple of 3, which is the default TCP packet retransmission window.
        conn_timeout = target.timeout
        # Once your client has connected to the server and sent the HTTP request, the read timeout
        # is the number of seconds the client will wait for the server to send a response.
        # (Specifically, it’s the number of seconds that the client will wait between bytes sent
        # from the server.
        read_timeout = target.timeout
        return (conn_timeout, read_timeout)
