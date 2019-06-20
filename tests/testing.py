"""
Utilities for testing libraries using Aloe.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin
from builtins import super
# pylint:enable=redefined-builtin

import io
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from functools import wraps
import pytest
import glob
import shutil

from aloe import world
from aloe.fs import path_to_module_name
from aloe.registry import (
    CALLBACK_REGISTRY,
    PriorityClass,
    STEP_REGISTRY,
)
from aloe.utils import PY3, StreamTestWrapperIO

# When the outer Nose captures output, it's a different type between Python 2
# and 3.
if PY3:
    CAPTURED_OUTPUTS = (io.StringIO,)
else:
    # io.StringIO is an alias to cStringIO.StringIO, which is a function and
    # not a type
    import StringIO  # pylint:disable=import-error
    CAPTURED_OUTPUTS = (
        type(io.StringIO()),
        StringIO.StringIO,
    )

def in_directory(directory):
    """
    A decorator to change the current directory and add the new one to the
    Python module search path.

    Upon exiting, the directory is changed back, the module search path change
    is reversed and all modules loaded from the directory are removed from
    sys.modules.

    Applies to either a function or an instance of
    TestCase, in which case setUp/tearDown are used.
    """
    
    def wrapper(func_or_class):
        """
        Wrap a function or a test case class to execute in a different
        directory.
        """

        try:
            is_test_case = issubclass(func_or_class, unittest.TestCase)
        except TypeError:
            is_test_case = False

        if is_test_case:
            
            func_or_class.test_dir = os.path.abspath(directory)

            return func_or_class

        else:
            # Wrap a function
            @wraps(func_or_class)
            def wrapped(*args, **kwargs):
                """
                Execute the function in a different directory.
                """
                
                return func_or_class(*args, **kwargs)

            return wrapped

    return wrapper


@contextmanager
def named_temporary_file(*args, **kwargs):
    """
    Create a named temporary file that is removed on exiting the context
    manager.
    """

    kwargs['delete'] = False
    with tempfile.NamedTemporaryFile(*args, **kwargs) as file_:
        try:
            yield file_
        finally:
            try:
                os.unlink(file_.name)
            except OSError:
                pass

class FeatureTest(unittest.TestCase):
    """
    Base class for tests running Gherkin features.
    """

    def setUp(self):
        """
        Ensure inner Nose doesn't redirect output.
        """

        os.environ['NOSE_NOCAPTURE'] = '1'

    @pytest.fixture(autouse=True)
    def inittestdir(self, testdir):
        self.testdir = testdir        

        features_dir = os.path.join(self.test_dir, "features") 
        
        steps_file = os.path.join(features_dir, "steps.py") 
        if (os.path.isfile(steps_file)):
            with open(steps_file, 'r') as file:
                testdir.makeconftest(file.read())  

        files = glob.iglob(os.path.join(features_dir, "*.feature"))
        dest_dir = testdir.mkdir("features");
        for file in files:
            if os.path.isfile(file):                
                shutil.copy(file, dest_dir)      
        

    def run_feature_string(self, feature_string, pytest_args = None):
        """
        Run the specified string as a feature.

        The feature will be created as a temporary file in the 'features'
        directory relative to the current directory. This ensures the steps
        contained within would be found by the loader.
        """
        
        self.testdir.makefile(".feature", feature_string)  

        filename = self._testMethodName + ".feature"
        return self.run_features(filename);
        # self.testdir.inline_run(filename, plugins=["pytest_eucalyptus"])
        # return TestResult(result)


    def run_features(self, *args, **kwargs):
        """
        Run the specified features.
        """

        # named keyword args and variable positional args aren't supported on
        # Python 2
        verbosity = kwargs.get('verbosity')
        stream = kwargs.get('stream')
        force_color = kwargs.get('force_color', False)

        if stream is None:       
            # redirects output
            stream = StreamTestWrapperIO()

        # Reset the state of callbacks and steps so that individual tests don't
        # affect each other
        CALLBACK_REGISTRY.clear(priority_class=PriorityClass.USER)
        STEP_REGISTRY.clear()
        world.__dict__.clear()
        
        old_stdout = sys.stdout        
        sys.stdout = stream
        
        result = self.testdir.inline_run(*args, plugins=["pytest_eucalyptus"])
        sys.stdout = old_stdout        
        return TestResult(result, stream);
        

    def assert_feature_success(self, *features, **kwargs):
        """
        Assert that the specified features can be run successfully.
        """

        result = self.run_features(*features, **kwargs)
        try:
            assert result.success
            return result
        except AssertionError:
            if isinstance(result.captured_stream, CAPTURED_OUTPUTS):
                print("--Output--")
                print(result.captured_stream.getvalue())
                print("--END--")
            raise    
            pass        

    def assert_feature_fail(self, *features, **kwargs):
        """
        Assert that the specified features fail when run.
        """

        result = self.run_features(*features, **kwargs)
        try:
            assert not result.success
            return result
        except AssertionError:
            if isinstance(result.captured_stream, CAPTURED_OUTPUTS):
                print("--Output--")
                print(result.captured_stream.getvalue())
                print("--END--")
            raise
            pass


class TestResult(object):
    def __init__(self, result, stream):
        realpassed, realskipped, realfailed = result.listoutcomes();
        self.success = len(realskipped) == 0 and len(realfailed) == 0
        self.captured_stream = stream        