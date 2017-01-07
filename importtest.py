#!/usr/bin/env python2.7
from __future__ import absolute_import, print_function
import sys
print("sys.path=%r" % (sys.path,))

import cracklib
import distutils
import zappa.handler

def main(event, context):
    return {}
