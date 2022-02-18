from .base_au import BaseAU
from .pip_github_au import PipGitHubAU
from .pip_au import PipAU

from zetuptools import PipPackage

package_name = "au"

__version__ = '0.0.0'
if __version__ == "0.0.0":
    try:
        __version__ = PipPackage(package_name).version
    except FileNotFoundError:
        pass
