"""Main file for redbox_exporter."""

from typing import Callable, Any

import concurrent.futures
import os
import sys
import threading
import time
import timeit

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from .args import *
from .config import *
from .request import *
from .prometheus import *


class Handler(BaseHTTPRequestHandler):
    """Simple webserver to serve metrics."""

    def __init__(self, cfg: DsConfig, req: Request, *args: Any, **kwargs: Any) -> None:
        self.cfg = cfg
        self.req = req
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    homepage = """<html>
  <head>
  </head>
  <body>
    <h1>{DEF_NAME}</h1>
    <p>{DEF_DESC}</p>
    <ul>
      <li><strong>Name:</strong> <code>{DEF_NAME}</code></li>
      <li><strong>Version:</strong> {DEF_VERSION}</li>
      <li><strong>Author:</strong> <a href="https://github.com/{DEF_AUTHOR}">{DEF_AUTHOR}</a></li>
      <li><strong>GitHub:</strong> <a href="{DEF_GITHUB}">{DEF_GITHUB}</a></li>
    </ul>
    <p>Go to <a href="/metrics">/metrics</a> to access metrics.</p>
  </body>
</html>""".format(
        DEF_NAME=DEF_NAME,
        DEF_DESC=DEF_DESC,
        DEF_VERSION=DEF_VERSION,
        DEF_AUTHOR=DEF_AUTHOR,
        DEF_GITHUB=DEF_GITHUB,
    )

    def do_GET(self) -> None:  # # pylint: disable=invalid-name
        """Serves GET requests."""
        time_calling_start = timeit.default_timer()

        # Display homepage
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.homepage.encode() + b"\n")
            return
        # We don't have a favicon
        if self.path == "/favicon.ico":
            self.send_response(404)
            self.end_headers()
            return
        # Redirect on wrong paths
        if self.path != "/metrics":
            self.send_response(302)
            self.send_header("Location", "/metrics")
            self.end_headers()
            return

        # Check targets for their http response
        # Run threaded so the time taken is not summed up by each defined target.
        responses = []
        config = self.cfg
        request = self.req

        targets = config.targets
        timeout = config.scrape_timeout
        executor = concurrent.futures.ThreadPoolExecutor()
        future_tasks = {executor.submit(request.request, target): target for target in targets}
        time_threads_start = timeit.default_timer()
        has_timeout = False
        try:
            for future in concurrent.futures.as_completed(future_tasks, timeout=timeout):
                responses.append(future.result())
        except concurrent.futures.TimeoutError:
            has_timeout = True
            time_threads_end = timeit.default_timer()
            print(
                "Threads timed out after: {0:.6f} sec".format(
                    time_threads_end - time_threads_start
                ),
                file=sys.stderr,
            )
        else:
            time_threads_end = timeit.default_timer()

        # If we encountered a thread timeout, we fill up all targets which had a timeout
        # with default values and a timeout error;
        if has_timeout:
            for desired in targets:
                desired_name = desired.name
                need_to_add = True
                for actual in responses:
                    actual_name = actual.name
                    if desired_name == actual_name:
                        need_to_add = False
                        break
                if need_to_add:
                    responses.append(
                        request.build_failed_response(
                            desired,
                            "Timeout: Scrape timeout after {0:.6f}s".format(
                                time_threads_end - time_threads_start
                            ),
                        )
                    )

        # Convert to prometheus format
        time_metrics_start = time_threads_end
        metrics = get_prom_format(responses)
        time_metrics_end = timeit.default_timer()

        # Send response to scraper
        time_serving_start = time_metrics_end
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(metrics.encode() + b"\n")
        time_serving_end = timeit.default_timer()

        # Add timing information for logging
        print("Threads: {0:.5f}s".format(time_threads_end - time_threads_start), file=sys.stderr)
        print("Convert: {0:.5f}s".format(time_metrics_end - time_metrics_start), file=sys.stderr)
        print("Respond: {0:.5f}s".format(time_serving_end - time_serving_start), file=sys.stderr)
        print("Overall: {0:.5f}s".format(time_serving_end - time_calling_start), file=sys.stderr)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """Implement a threaded HTTP server.

    https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
    """

    # def __init__(self, digest_auth_handler, *args, **kwargs):
    #    # This has to be set before calling our parent's __init__(), which will
    #    # try to call do_GET().
    #    self.digest_auth_handler = digest_auth_handler
    #    BaseHTTPRequestHandler.__init__(self, *args, **kwargs)


def run_webserver(conf: DsConfig) -> None:
    """Run webserver to serve metrics."""
    print(time.asctime(), "Starting webserver on {}:{}".format(conf.listen_addr, conf.listen_port))
    # Initialize and run web server

    def handler_with_extra_args(cfg: DsConfig, req: Request) -> Callable[[Any], Handler]:
        return lambda *args: Handler(cfg, req, *args)

    # Make conf variable available in Handler
    req = RequestSimple()

    try:
        server = ThreadingSimpleServer(
            (conf.listen_addr, conf.listen_port), handler_with_extra_args(conf, req)
        )
    except OSError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
    # Serve
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    # Shutdown
    server.server_close()
    print(time.asctime(), "Server Stopped")


def main() -> None:
    """Run main entrypoint."""
    cmd_args = get_args()

    # Get configuration
    try:
        conf = get_config(cmd_args)
    except OSError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    # Initialize and run web server
    run_webserver(conf)


if __name__ == "__main__":
    main()
