import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import packaging.version
import zmtools


class UpdateException(Exception):
    # Base exception class for this module
    pass


class BaseAU:
    """Base auto-updater. Should be inherited from.

    Attributes:
        current_version (str): The current version of the package.
        latest_version (str): The latest version of the package.
        needs_update (bool): If the package is not the latest version.
    """

    def __init__(self) -> None:
        self.current_version = self._get_current_version()
        self.latest_version = self._get_latest_version()

    def _get_current_version(self) -> str:  # type: ignore
        # Override me!
        # This function must return the current version of the package
        pass

    def _get_latest_version(self) -> str:  # type: ignore
        # Override me!
        # This function must return the latest version of the package
        pass

    def _download(self) -> Path:  # type: ignore
        # Override me!
        # This function must download the package and return the path of the downloaded file
        pass

    def _update(self, update_file: Path) -> None:
        # Override me!
        # This function must install a package whose location is passed via the sole parameter
        pass

    def update(self, prompt: bool = True) -> None:
        """Update the package.

        Args:
            prompt (bool, optional): If True, prompt before updating. Defaults to True.
        """
        if self.needs_update and (
            not prompt
            or zmtools.y_to_continue(
                f"A newer version ({self.latest_version}) is available. Would you like to update?"
            )
        ):
            with TemporaryDirectory() as temp_dir:
                with zmtools.working_directory(Path(temp_dir)):
                    update_file = self._download()
                    self._update(update_file)
            print("Exiting as an update has completed")
            sys.exit()

    @property
    def currently_installed_version_is_unreleased(self) -> bool:
        # Override me!
        # This property should return True if the currently installed version of a package is in development, i.e. an unreleased commit
        return False

    @property
    def needs_update(self) -> bool:
        if (
            self.current_version == "0.0.0"
            or self.currently_installed_version_is_unreleased
        ):
            return False
        else:
            return packaging.version.parse(
                self.latest_version
            ) > packaging.version.parse(self.current_version)
