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
from pathlib import Path
import glob
from distutils.dir_util import copy_tree

from aloe import world
from aloe.fs import path_to_module_name
from aloe.registry import (
    CALLBACK_REGISTRY,
    PriorityClass,
    STEP_REGISTRY,
)
from aloe.utils import PY3, TestWrapperIO

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
        # copy_tree(self.test_dir, self.testdir.tmpdir.strpath) 

        # copy steps.py as conftest.py
                # copy 
        steps_file = os.path.join(self.test_dir, "features/steps.py") 
        if (os.path.isfile(steps_file)):
            with open(steps_file, 'r') as file:
                testdir.makeconftest(file.read())
        # imports = []
        # # if (filename.suffix == ".feature" or filename.name == "steps"):
        # for filename in Path(self.testdir.tmpdir.strpath).glob('**/steps.py'):                    
        #     # dir = os.path.dirname(filename)
        #     relative_path = os.path.relpath(filename, self.testdir.tmpdir.strpath)            
        #     # os.path.ensure(relative_dir)

        # #     dir = os.path.dirname(filename)
        # #     relative_dir = os.path.relpath(dir, self.testdir.tmpdir.strpath)
        #     import_steps = relative_path[:-3].replace(os.sep, ".") # + ".steps" if relative_dir else "steps"
        # #     # if (relative_dir.startswith(".")):
        # #     #     relative_dir = relative_dir[1:]
        #     imports.append(f"import {import_steps}")
        # #     with open(filename, 'r') as ile
        # # #         sub_dir = testdir.mkdir(relative_dir)
        # #     sub_dir.makeconftest(file.read())
        # testdir.makeconftest(imports)
        # testdir.chdir()

        # copy feature files
        # files = glob.iglob(os.path.join(source_dir, "*.*"))
        # for file in files:
        #     if os.path.isfile(file):
        #         shutil.copy2(file, dest_dir)
        

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
        # self.testdir.inline_run(filename, plugins=["pytest_aloe"])
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

        if stream is None and isinstance(sys.stdout, CAPTURED_OUTPUTS):
            # Don't show results of running the inner tests if the outer Nose
            # redirects output
            stream = TestWrapperIO()

        # Reset the state of callbacks and steps so that individual tests don't
        # affect each other
        CALLBACK_REGISTRY.clear(priority_class=PriorityClass.USER)
        STEP_REGISTRY.clear()
        world.__dict__.clear()

        # argv = ['aloe']

        # if verbosity:
        #     argv += ['--verbosity', str(verbosity)]

        # if force_color:
        #     argv += ['--color']

        # argv += list(features)

        # Save the loaded module list to restore later
        # old_modules = set(sys.modules.keys())

        # result = TestRunner(exit=False, argv=argv, stream=stream)
        # result.captured_stream = stream

        # # To avoid affecting the (outer) testsuite and its subsequent tests,
        # # unload all modules that were newly loaded. This also ensures that they
        # # are loaded again for the next tests, registering relevant steps and
        # # hooks.
        # new_modules = set(sys.modules.keys())
        # for module_name in new_modules - old_modules:
        #     del sys.modules[module_name]
        
        # run empty
        # if (not args):
        result = self.testdir.inline_run(*args, plugins=["pytest_aloe"])
        return TestResult(result);

        # # run specific test
        # feature = list(args)[0]
        # args = " ".join(list(args)[1:])
        # feature_file = os.path.join(self.test_dir, feature)
        # feature_string = ""
        # with open(feature_file, 'r') as file:
        #     feature_string = file.read()

        # return self.run_feature_string(feature_string, args)        
        

    def assert_feature_success(self, *features, **kwargs):
        """
        Assert that the specified features can be run successfully.
        """

        result = self.run_features(*features, **kwargs)
        try:
            assert result.success
            return result
        except AssertionError:
            # if isinstance(result.captured_stream, CAPTURED_OUTPUTS):
            #     print("--Output--")
            #     print(result.captured_stream.getvalue())
            #     print("--END--")
            # raise
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
            # if isinstance(result.captured_stream, CAPTURED_OUTPUTS):
            #     print("--Output--")
            #     print(result.captured_stream.getvalue())
            #     print("--END--")
            # raise
            pass


class TestResult(object):
    def __init__(self, result):
        self.success = result.ret == 0
        # self.captured_stream = self.stdout