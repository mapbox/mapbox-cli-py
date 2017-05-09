# This module allows the Mapbox CLI to be invoked more quickly
# without scanning the PYTHONPATH for 'console_script' entry points.
# Usage:
#
# $ python -m mapboxcli --help

import sys

from mapboxcli.scripts.cli import main_group

sys.exit(main_group())
