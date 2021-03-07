import importlib
import requests
import subprocess
import sys

from zetuptools import PipPackage

from .base_au import BaseAU


class PipAU(BaseAU):

    def __init__(self, name, silent=False):
        self._pip_package = PipPackage(name)
        self.silent = silent
        super().__init__()

    @property
    def _o(self):
        if self.silent:
            return subprocess.DEVNULL
        else:
            return None

    def _get_current_version(self):
        return self._pip_package.version

    def _get_latest_version(self):
        return requests.get(f"https://pypi.org/pypi/{self._pip_package.name}/json").json()["info"]["version"]

    def _update(self, update_file):
        subprocess.run([sys.executable, "-m", "pip", "install",
                        f"{self._pip_package.name}=={self.latest_version}"], stdout=self._o)
        try:
            importlib.import_module(
                f"{self._pip_package.name}.install_directives")
            has_id = True
        except ModuleNotFoundError:
            has_id = False
        if has_id:
            subprocess.run(
                ["install-directives", self._pip_package.name, "install"])
