# -*- coding: utf-8 -*-

import os
from pathlib import Path

import pytest
from aloe.testclass import TestCase, TestScenario
from aloe.registry import CALLBACK_REGISTRY
from gherkin.parser import Parser
from pytest import Collector, File, Item
from _pytest.unittest import TestCaseFunction
from importlib import import_module

def pytest_addoption(parser):
    group = parser.getgroup('pytest-aloe')
    group.addoption(
        '--tags',
        action='store',
        dest='tags',
        default='',
        help='Set tags to run.'
    )

    test_class_name = \
            '{c.__module__}.{c.__name__}'.format(c=TestCase)            

    group.addoption( 
        '--test-class',
        action='store',
        dest='test_class_name',
        default=os.environ.get('GHERKIN_CLASS', test_class_name),
        metavar='TEST_CLASS',
        help='Base class to use for the generated tests',
    )

    # parser.addini('HELLO', 'Dummy pytest.ini setting')


def pytest_collect_file(path, parent):
    """
    Collection hook for py.test
    This collection hook looks for .feature files which contain cucumber tests.
    """
    if path.ext == '.feature':
        return Feature(path, parent)


class Feature(File):
    def collect(self):
        module_name, class_name = self.config.option.test_class_name.rsplit('.', 1)
        test_class_module = import_module(module_name)
        test_class = getattr(test_class_module, class_name)

        test_case = test_class.from_file(self.fspath.strpath)     
        self.obj = test_case
        functions = [TestCaseFunction(scenario, parent=self) for scenario in test_case.scenarios]
        test_case.functions = functions
        for function in functions:
            yield function

@pytest.fixture(autouse=True, scope='session')
def session_hooks():
    before_all, after_all = CALLBACK_REGISTRY.before_after('all')
    # setup_stuff
    before_all()                
    yield
    # teardown_stuff
    after_all()