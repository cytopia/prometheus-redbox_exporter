"""Parse command line arguments."""

import argparse

from .defaults import DEF_NAME, DEF_DESC, DEF_VERSION, DEF_AUTHOR, DEF_GITHUB
from .defaults import DEF_SRV_LISTEN_ADDR, DEF_SRV_LISTEN_PORT


def _get_version():
    # type: () -> str
    """Return version information."""
    return """%(prog)s: Version %(version)s
(%(url)s) by %(author)s""" % (
        {"prog": DEF_NAME, "version": DEF_VERSION, "url": DEF_GITHUB, "author": DEF_AUTHOR}
    )


def get_args() -> argparse.Namespace:
    """Retrieve command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        usage="""%(prog)s [options] -c CONF
       %(prog)s -v, --version
       %(prog)s -h, --help"""
        % ({"prog": DEF_NAME}),
        description=DEF_DESC,
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    misc = parser.add_argument_group("misc arguments")

    required.add_argument(
        "-c", "--conf", type=str, required=True, help="""Specify path to configuration file."""
    )
    optional.add_argument(
        "-l",
        "--listen",
        metavar="ADDR",
        type=str,
        default=DEF_SRV_LISTEN_ADDR,
        help="""Override listen address from configuration file.
Defaults to {} if neither, cmd argument or config settings exist.""".format(
            DEF_SRV_LISTEN_ADDR
        ),
    )
    optional.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEF_SRV_LISTEN_PORT,
        help="""Override listen port from configuration file.
Defaults to {} if neither, cmd argument or config settings exist.""".format(
            DEF_SRV_LISTEN_PORT
        ),
    )
    misc.add_argument(
        "-v",
        "--version",
        action="version",
        version=_get_version(),
        help="Show version information and exit",
    )
    misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    # Return arguments
    return parser.parse_args()
