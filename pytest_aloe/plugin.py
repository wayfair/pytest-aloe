# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from aloe.testclass import TestCase, TestScenario
from gherkin.parser import Parser
from pytest import Collector, File, Item


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

def pytest_pycollect_makeitem(collector, name, obj):
    pass

def pytest_collect_file(path, parent):
    """Collection hook for py.test

    This collection hook looks for Yaml files which may contain tests. The
    files themselves must be of the glob: `test*.yml`. Once discovered the
    test files are collected into a multiple hierarchy of
    :class:`py.test.collect.Item` which is described in detail in the module
    documentation.
    """
    if path.ext == '.feature':
        
        return Feature(path, parent)

class Feature(File):
    """    
    """

    def collect(self):

        test_case = TestCase.from_file(self.fspath.strpath)       

        return [Scenario(scenario.name, test_case, self) for scenario in test_case.feature.scenarios]

class Scenario(Item):
    def __init__(self, scenario_name, test_case, parent):
        super(Scenario, self).__init__(scenario_name, parent)           
        self.test_case = test_case     

    def runtest(self):
        scenario = self.test_case(self.name)                
        result = scenario.run()        
        if (result.errors):
            raise GenericError(result.errors)        

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """               
        return excinfo.value.errors[0][1];

    def reportinfo(self):
        return self.fspath, None, self.name


class GenericError(Exception):

    def __init__(self, errors):
        self.errors = errors