# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from contextlib import contextmanager

from yamlns.testutils import assertNsEqual
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path # Py2

# Readable verbose testcase listing
unittest.TestCase.__str__ = unittest.TestCase.id

def _inProduction():
    import erppeek_wst
    import dbconfig
    c = erppeek_wst.ClientWST(**dbconfig.erppeek)
    c.begin()
    destructive_testing_allowed = c._execute(
        'res.config', 'get', 'destructive_testing_allowed', False)
    c.rollback()
    c.close()

    if destructive_testing_allowed: return False
    return True

def destructiveTest(decorated):
    return unittest.skipIf(_inProduction(),
        "Destructive test being run in a production setup!!")(decorated)

@contextmanager
def temp_path():
    """
    Context manager that creates a temporary dir and ensures
    that all the content is removed after the with scope
    Returns the pathlib Path of the created dir.

    >>> with temp_path() as tmp:
    ...     mypath = tmp / 'myfile'
    ...     nbytes = mypath.write_text('hello world', encoding='utf8')
    ...     # TODO: remove the str bellow when Py2 dropped
    ...     str(mypath.read_text(encoding='utf8')) # returns "hello world"
    ...     assert mypath.exists(), "Should exists at this point"
    'hello world'

    >>> assert not mypath.exists(), "Sould not exist at this point"

    It will clean up even after raising an exception

    >>> with temp_path() as tmp:
    ...     mypath = tmp / 'myfile'
    ...     nbytes = mypath.write_text('hello world', encoding='utf8')
    ...     assert mypath.exists(), "Should exists at this point"
    ...     raise Exception("This will interrupt the code")
    Traceback (most recent call last):
        ...
    Exception: This will interrupt the code

    >>> assert not mypath.exists(), "Sould not exist at this point"
    """

    import shutil
    import tempfile

    path = Path(tempfile.mkdtemp())
    shutil.rmtree(str(path), ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(str(path), ignore_errors=True)



# vim: ts=4 sw=4 et
