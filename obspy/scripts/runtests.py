#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A command-line program that runs all ObsPy tests.

All tests in ObsPy are located in the tests directory of the each specific
module. This script is a simple wrapper which changes directory to ObsPy's
base directory then simply passes all input params to pytest. The intention
of this script is to make it easy for users to test their installation of
ObsPy. When working on ObsPy development it is recommend to use pytest
directly.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)

.. rubric:: Examples

(1) Run all local tests (ignoring tests requiring a network connection) on
    command line::

        $ obspy-runtests

(2) Run all tests on command line::

        $ obspy-runtests --all

(3) Verbose output::

        $ obspy-runtests -v

(4) Run tests of module :mod:`obspy.io.mseed`::

        $ obspy-runtests io/mseed

(5) Run tests of multiple modules, e.g. :mod:`obspy.io.wav` and
    :mod:`obspy.io.sac`::

        $ obspy-runtests io/wav io/sac

(6) Run a specific test case::

        $ obspy-runtests obspy.core.tests.test_stats.StatsTestCase.test_init

(7) Report test results to https://tests.obspy.org/::

        $ obspy-runtests -r

(8) To get a full list of all pytest options, use::

        $ obspy-runtests --help

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import sys
import warnings
from os.path import dirname

import numpy as np

from obspy.testing.testrunner import run_tests


# make sure a __file__ exists
if not hasattr(sys.modules[__name__], '__file__'):
    __file__ = inspect.getfile(inspect.currentframe())


def main(argv=''):
    """
    Entry point for setup.py.

    Wrapper for a profiler if requested otherwise just call run() directly.
    If profiling is enabled we disable interactivity as it would wait for user
    input and influence the statistics. However the -r option still works.
    """
    # catch and ignore a NumPy deprecation warning
    with warnings.catch_warnings(record=True):
        warnings.filterwarnings(
            "ignore", 'The compiler package is deprecated and removed in '
                      'Python 3.x.', DeprecationWarning)
        np.safe_eval('1')
    # set obspy's current directory as rootdir
    obspy_base_path = dirname(dirname(__file__))
    # run tests, collect errors
    errors = run_tests(argv, rootdir=obspy_base_path)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
