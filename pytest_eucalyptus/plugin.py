# -*- coding: utf-8 -*-

import os

import pytest
from aloe.testclass import TestCase, TestScenario
from aloe.registry import CALLBACK_REGISTRY
from gherkin.parser import Parser
from pytest import Collector, File, Item
from _pytest.unittest import TestCaseFunction, UnitTestCase
from _pytest.compat import getimfunc
from importlib import import_module
import sys


def pytest_addoption(parser):
    group = parser.getgroup("pytest-aloe")
    group.addoption("--tags", action="store", dest="tags", default="", help="Set tags to run.")

    test_class_name = "{c.__module__}.{c.__name__}".format(c=TestCase)

    group.addoption(
        "--test-class",
        action="store",
        dest="test_class_name",
        default=os.environ.get("GHERKIN_CLASS", test_class_name),
        metavar="TEST_CLASS",
        help="Base class to use for the generated tests",
    )
    group.addoption(
        "--scenario-indices",
        action="store",
        dest="scenario_indices",
        default="",
        help="Only run scenarios with these indices (comma-separated)",
    )

    # parser.addini('HELLO', 'Dummy pytest.ini setting')


def pytest_collect_file(path, parent):
    """
    Collection hook for py.test
    This collection hook looks for .feature files which contain cucumber tests.
    """
    if path.ext == ".feature":
        return Feature(path, parent)


class Feature(File):
    def collect(self):

        module_name, class_name = self.config.option.test_class_name.rsplit(".", 1)
        test_class_module = import_module(module_name)
        test_class = getattr(test_class_module, class_name)

        test_case = test_class.from_file(self.fspath.strpath)
        self.obj = test_case

        unit_test_case = FeatureUnitTestCase(test_case.feature.name, parent=self)
        unit_test_case.obj = test_case
        return [unit_test_case]


class FeatureUnitTestCase(UnitTestCase):
    def collect(self):

        cls = self.obj
        if not getattr(cls, "__test__", True):
            return

        skipped = getattr(cls, "__unittest_skip__", False)
        if not skipped:
            self._inject_setup_teardown_fixtures(cls)
            self._inject_setup_class_fixture()

        self.session._fixturemanager.parsefactories(self, unittest=True)

        for name in self.obj.scenarios:
            x = getattr(self.obj, name)
            if not getattr(x, "__test__", True):
                continue
            funcobj = getimfunc(x)
            function = TestCaseFunction(name, parent=self, callobj=funcobj)
            self.obj.functions.append(function)
            yield function
            foundsomething = True


@pytest.fixture(autouse=True, scope="session")
def session_hooks():
    before_all, after_all = CALLBACK_REGISTRY.before_after("all")
    # setup_stuff
    before_all()
    yield
    # teardown_stuff
    after_all()


def pytest_collection_modifyitems(items, config):
    scenario_indices = config.getoption("scenario_indices")
    if not scenario_indices:
        return

    remaining = []
    deselected = []
    indices = [int(str) for str in scenario_indices.split(",")]
    for colitem in items:
        index = colitem.obj.scenario_index
        if index not in indices:
            deselected.append(colitem)
        else:
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining
