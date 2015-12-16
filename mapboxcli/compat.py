# compatibility module.

import itertools
import sys

from six.moves import configparser


map = itertools.imap if sys.version_info < (3,) else map

