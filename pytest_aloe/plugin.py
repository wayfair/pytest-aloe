# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from aloe.testclass import TestCase, TestScenario
from gherkin.parser import Parser
from pytest import Collector, File, Item
from _pytest.unittest import TestCaseFunction

def pytest_addoption(parser):
    group = parser.getgroup('aloe')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2019',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo

def pytest_collect_file(path, parent):
    """
    Collection hook for py.test
    This collection hook looks for .feature files which contain cucumber tests.
    """    
    if path.ext == '.feature':        
        return Feature(path, parent)

class Feature(File):
    def collect(self):
        test_case = TestCase.from_file(self.fspath.strpath)     
        self.obj = test_case
        functions = [TestCaseFunction(scenario.name, parent=self) for scenario in test_case.feature.scenarios]
        for function in functions:
            test_case.request = function._request;
            yield function