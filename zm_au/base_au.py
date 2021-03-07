import sys
from tempfile import TemporaryDirectory

import packaging.version
import zmtools


class UpdateException(Exception):
    # Base exception class for this module
    pass


class BaseAU():

    """Base auto-updater class. Will not work as is; its purpose is to be inherited from

    Attributes:
        current_version (str): The current version of the package
        latest_version (str): The latest version of the package
        needs_update (bool): If the package is not the latest version
    """

    def __init__(self):
        self.current_version = self._get_current_version()
        self.latest_version = self._get_latest_version()

    def _get_current_version(self):
        # Override me!
        # This function must return the current version of the package
        pass

    def _get_latest_version(self):
        # Override me!
        # This function must return the latest version of the package
        pass

    def _download(self):
        # Override me!
        # This function must download the package and return the filename of the downloaded file
        pass

    def _update(self, update_file):
        # Override me!
        # This function must install a package whose location is passed via the sole parameter
        pass

    def update(self, prompt=True):
        """Update the package

        Args:
            prompt (bool, optional): If True, prompt before updating. Defaults to True.
        """
        if self.needs_update and (not prompt or zmtools.y_to_continue(f"A newer version ({self.latest_version}) is available. Would you like to update?")):
            with TemporaryDirectory() as temp_dir:
                with zmtools.working_directory(temp_dir):
                    update_file = self._download()
                    self._update(update_file)
            print("Exiting as an update has completed")
            sys.exit()

    @property
    def needs_update(self):
        return packaging.version.parse(self.latest_version) > packaging.version.parse(self.current_version)
