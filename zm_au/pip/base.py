import importlib
import os
import subprocess
import sys
from typing import Optional, Union

import packaging.version
import requests
from python_install_directives import PipPackage

from ..base import BaseAU


class PipAU(BaseAU):
    def __init__(self, name: str, silent: bool = False) -> None:
        self._pip_package = PipPackage(name)
        self.silent = silent
        super().__init__()

    @property
    def _o(self) -> Optional[int]:
        # If silent, redirect output of pip to the null device
        if self.silent:
            return subprocess.DEVNULL
        else:
            return None

    def _get_current_version(self) -> str:
        return self._pip_package.version

    def _get_latest_version(self) -> str:
        # Hits the PyPI API to find the latest version
        return requests.get(
            f"https://pypi.org/pypi/{self._pip_package.name}/json"
        ).json()["info"]["version"]

    def _update(self, update_file: Union[os.PathLike, str]) -> None:
        # Runs a `pip install` of the version found by _get_latest_version (doesn't blindly install the latest version to avoid weird race conditions)
        # Note that _download was never overridden. It does not need to be as that functionality is built into `pip install`
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                f"{self._pip_package.name}=={self.latest_version}",
            ],
            stdout=self._o,
        )
        try:
            importlib.import_module(
                f"{self._pip_package.name}.python_install_directives"
            )
        except ModuleNotFoundError:
            has_id = False
        else:
            has_id = True
        if has_id:
            subprocess.run(["install-directives", self._pip_package.name, "install"])

    @property
    def currently_installed_version_is_unreleased(self) -> bool:
        return bool(packaging.version.parse(self.current_version).local)
