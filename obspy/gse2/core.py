# -*- coding: utf-8 -*-
"""
GSE2/GSE1 bindings to ObsPy core module.
"""

from __future__ import unicode_literals
from obspy import Trace, Stream
from obspy.gse2 import libgse2, libgse1
import numpy as np


def isGSE2(filename):
    """
    Checks whether a file is GSE2 or not.

    :type filename: string
    :param filename: GSE2 file to be checked.
    :rtype: bool
    :return: ``True`` if a GSE2 file.
    """
    # Open file.
    try:
        with open(filename, 'rb') as f:
            libgse2.isGse2(f)
    except:
        return False
    return True


def readGSE2(filename, headonly=False, verify_chksum=True,
             **kwargs):  # @UnusedVariable
    """
    Reads a GSE2 file and returns a Stream object.

    GSE2 files containing multiple WID2 entries/traces are supported.

    .. warning::
        This function should NOT be called directly, it registers via the
        ObsPy :func:`~obspy.core.stream.read` function, call this instead.

    :type filename: string
    :param filename: GSE2 file to be read.
    :type headonly: boolean, optional
    :param headonly: If True read only head of GSE2 file.
    :type verify_chksum: boolean, optional
    :param verify_chksum: If True verify Checksum and raise Exception if
        it is not correct.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream object containing header and data.

    .. rubric:: Example

    >>> from obspy import read
    >>> st = read("/path/to/loc_RJOB20050831023349.z")
    """
    traces = []
    with open(filename, 'rb') as f:
        # reading multiple gse2 parts
        while True:
            try:
                if headonly:
                    header = libgse2.readHeader(f)
                    traces.append(Trace(header=header))
                else:
                    header, data = libgse2.read(f, verify_chksum=verify_chksum)
                    traces.append(Trace(header=header, data=data))
            except EOFError:
                break
    return Stream(traces=traces)


def writeGSE2(stream, filename, inplace=False, **kwargs):  # @UnusedVariable
    """
    Write GSE2 file from a Stream object.

    .. warning::
        This function should NOT be called directly, it registers via the
        the :meth:`~obspy.core.stream.Stream.write` method of an
        ObsPy :class:`~obspy.core.stream.Stream` object, call this instead.

    :type stream: :class:`~obspy.core.stream.Stream`
    :param stream: The ObsPy Stream object to write.
    :type filename: string
    :param filename: Name of file to write.
    :type inplace: boolean, optional
    :param inplace: If True, do compression not on a copy of the data but
        on the data itself - note this will change the data values and make
        them therefore unusable!

    .. rubric:: Example

    >>> from obspy import read
    >>> st = read()
    >>> st.write('filename.gse', format='GSE2') #doctest: +SKIP
    """
    #
    # Translate the common (renamed) entries
    with open(filename, 'wb') as f:
        # write multiple gse2 parts
        for trace in stream:
            dt = np.dtype('int32')
            if trace.data.dtype.name == dt.name:
                trace.data = np.require(trace.data, dt, ['C_CONTIGUOUS'])
            else:
                msg = "GSE2 data must be of type %s, but are of type %s" % \
                    (dt.name, trace.data.dtype)
                raise Exception(msg)
            libgse2.write(trace.stats, trace.data, f, inplace)


def isGSE1(filename):
    """
    Checks whether a file is GSE1 or not.

    :type filename: string
    :param filename: GSE1 file to be checked.
    :rtype: bool
    :return: ``True`` if a GSE1 file.
    """
    # Open file.
    with open(filename, 'rb') as f:
        try:
            data = f.readline()
        except:
            return False
    if data.startswith(b'WID1') or data.startswith(b'XW01'):
        return True
    return False


def readGSE1(filename, headonly=False, verify_chksum=True,
             **kwargs):  # @UnusedVariable
    """
    Reads a GSE1 file and returns a Stream object.

    GSE1 files containing multiple WID1 entries/traces are supported.

    .. warning::
        This function should NOT be called directly, it registers via the
        ObsPy :func:`~obspy.core.stream.read` function, call this instead.

    :type filename: string
    :type param: GSE2 file to be read.
    :type headonly: boolean, optional
    :param headonly: If True read only header of GSE1 file.
    :type verify_chksum: boolean, optional
    :param verify_chksum: If True verify Checksum and raise Exception if
        it is not correct.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream object containing header and data.

    .. rubric:: Example

    >>> from obspy import read
    >>> st = read("/path/to/y2000.gse")
    """
    traces = []
    # read GSE1 file
    with open(filename, 'rb') as fh:
        while True:
            try:
                if headonly:
                    header = libgse1.readHeader(fh)
                    traces.append(Trace(header=header))
                else:
                    header, data = \
                        libgse1.read(fh, verify_chksum=verify_chksum)
                    traces.append(Trace(header=header, data=data))
            except EOFError:
                break
    return Stream(traces=traces)
