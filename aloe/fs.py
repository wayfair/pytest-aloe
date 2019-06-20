# -*- coding: utf-8 -*-
"""
Filesystem-related utilities.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import fnmatch

from future.utils import raise_from

from aloe.exceptions import StepDiscoveryError


def path_to_module_name(filename):
    """Convert a path to a file to a Python module name."""

    filename = os.path.relpath(filename)

    dotted_path = []
    while True:
        filename, component = os.path.split(filename)
        dotted_path.insert(0, component)
        if filename == "":
            break

    dotted_path[-1] = os.path.splitext(dotted_path[-1])[0]
    if dotted_path[-1] == "__init__":
        dotted_path.pop()

    return ".".join(dotted_path)
