"""Converts response list into prometheus format."""

from typing import List, Dict, Any

from .types import DsResponse


METRIC_PREFIX = "redbox"


def __float2str(value: float) -> str:
    """Convert a float into a human readable string representatoin."""
    if value == 0.0:
        return "0.0"
    return "{0:.5f}".format(value)


def _get_metrics(responses: List[DsResponse], metric_settings: Dict[str, Any]) -> List[str]:
    """Wrapper function to get formated prometheus metrics."""
    m_name = metric_settings["name"]
    m_type = metric_settings["type"]
    m_help = metric_settings["help"]
    m_func = metric_settings["func"]

    metric = METRIC_PREFIX + "_" + m_name
    lines = [
        f"# HELP {metric} {m_help}",
        f"# TYPE {metric} {m_type}",
    ]

    for response in responses:
        name = response.name
        groups = ['group_{}="{}",'.format(key, response.groups[key]) for key in response.groups]
        url = response.url
        size = response.size
        time_ttfb = __float2str(response.time_ttfb)
        time_download = __float2str(response.time_download)
        time_render = __float2str(response.time_render)
        time_total = __float2str(response.time_total)
        status_code = response.status_code
        status_family = response.status_family
        success = "1" if response.success else "0"
        err_msg = response.err_msg
        extract = "\\n".join(response.extract)

        lines.append(
            f"{metric}{{"
            f'name="{name}",' + "".join(groups) + f'url="{url}",'
            f'bytes="{size}",'
            f'time_ttfb="{time_ttfb}",'
            f'time_download="{time_download}",'
            f'time_render="{time_render}",'
            f'time_total="{time_total}",'
            f'status_code="{status_code}",'
            f'status_family="{status_family}",'
            f'success="{success}",'
            f'err_msg="{err_msg}",'
            f'extract="{extract}"'
            "} " + m_func(response)
        )
    return lines


def _get_time_ttfb(responses: List[DsResponse]) -> List[str]:
    """Get formated TTFB time metrics."""
    metric_settings = {
        "name": "time_ttfb",
        "type": "untyped",
        "help": "Returns the TTFB time in seconds (time taken for headers to arrive).",
        "func": lambda response: __float2str(response.time_ttfb),
    }
    return _get_metrics(responses, metric_settings)


def _get_time_download(responses: List[DsResponse]) -> List[str]:
    """Get formated download time metrics."""
    metric_settings = {
        "name": "time_download",
        "type": "untyped",
        "help": "Returns the download time in seconds (time taken to download the body).",
        "func": lambda response: __float2str(response.time_download),
    }
    return _get_metrics(responses, metric_settings)


def _get_time_render(responses: List[DsResponse]) -> List[str]:
    """Get formated render time metrics."""
    metric_settings = {
        "name": "time_render",
        "type": "untyped",
        "help": "Returns the render time in seconds (time taken to HTML/JS render the body).",
        "func": lambda response: __float2str(response.time_render),
    }
    return _get_metrics(responses, metric_settings)


def _get_time_total(responses: List[DsResponse]) -> List[str]:
    """Get formated total time metrics."""
    metric_settings = {
        "name": "time_total",
        "type": "untyped",
        "help": "Returns the total time in seconds (time taken to request, render and download).",
        "func": lambda response: __float2str(response.time_total),
    }
    return _get_metrics(responses, metric_settings)


def _get_content_size(responses: List[DsResponse]) -> List[str]:
    """Get formated content size metrics."""
    metric_settings = {
        "name": "content_size",
        "type": "untyped",
        "help": "Returns the content size in bytes.",
        "func": lambda response: str(response.size),
    }
    return _get_metrics(responses, metric_settings)


def _get_failure(responses: List[DsResponse]) -> List[str]:
    """Get formated failure metrics."""
    metric_settings = {
        "name": "failure",
        "type": "untyped",
        "help": "Returns '1' if request or defined conditions fail or '0' on success.",
        "func": lambda response: "0" if response.success else "1",
    }
    return _get_metrics(responses, metric_settings)


def _get_success(responses: List[DsResponse]) -> List[str]:
    """Get formated success metrics."""
    metric_settings = {
        "name": "success",
        "type": "untyped",
        "help": "Returns '1' if request and defined conditions succeed or '0' on failure.",
        "func": lambda response: "1" if response.success else "0",
    }
    return _get_metrics(responses, metric_settings)


def _get_status_code(responses: List[DsResponse]) -> List[str]:
    """Get formated status code metrics."""
    metric_settings = {
        "name": "status_code",
        "type": "untyped",
        "help": "Returns the response http status code or '0' if request failed.",
        "func": lambda response: str(response.status_code),
    }
    return _get_metrics(responses, metric_settings)


def get_prom_format(responses: List[DsResponse]) -> str:
    """Format response list into prometheus format."""
    times_ttfb = _get_time_ttfb(responses)
    times_download = _get_time_download(responses)
    times_render = _get_time_render(responses)
    times_total = _get_time_total(responses)
    sizes = _get_content_size(responses)
    fails = _get_failure(responses)
    success = _get_success(responses)
    status_codes = _get_status_code(responses)
    return "\n".join(
        times_ttfb
        + times_download
        + times_render
        + times_total
        + sizes
        + fails
        + success
        + status_codes
    )
