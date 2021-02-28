"""Datatype definition."""

from typing import List

from ...types import DsTarget


class DsConfig:
    """Datastructure for config."""

    @property
    def scrape_timeout(self) -> int:
        """Scrape timeout."""
        return self.__scrape_timeout

    @property
    def listen_addr(self) -> str:
        """Listen address."""
        return self.__listen_addr

    @property
    def listen_port(self) -> int:
        """Listen port."""
        return self.__listen_port

    @property
    def targets(self) -> List[DsTarget]:
        """List of targets to check."""
        return self.__targets

    def __init__(
        self, scrape_timeout: int, listen_addr: str, listen_port: int, targets: List[DsTarget]
    ) -> None:
        self.__scrape_timeout = scrape_timeout
        self.__listen_addr = listen_addr
        self.__listen_port = listen_port
        self.__targets = targets
