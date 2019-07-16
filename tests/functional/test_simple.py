# -*- coding: utf-8 -*-
"""
Basic scenario tests.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import sys
import os
import unittest
from contextlib import contextmanager
from inspect import getsourcefile

# from nose.importer import Importer

from aloe import world
from aloe.exceptions import StepDiscoveryError

from tests.testing import (
    FeatureTest,
    in_directory,
)
from aloe.utils import PY3, StreamTestWrapperIO

# Pylint cannot infer the attributes on world
# pylint:disable=no-member


@in_directory('tests/simple_app')
class SimpleScenarioTest(FeatureTest):
    """
    Test that basic feature running works as expected.
    """

    def test_success(self):
        """
        Test running a simple feature.
        """

        self.assert_feature_success('features/calculator.feature')
    
    def test_exact_match(self):
        """
        Test running a simple feature.
        """

        self.assert_feature_success('features/exact_match.feature')

    def test_success_zh(self):
        """
        Test running a simple feature in Chinese.
        """

        self.assert_feature_success('features/calculator_zh.feature')

    def test_failure(self):
        """
        Test that a failing feature fails tests.
        """

        self.assert_feature_fail('features/wrong_expectations.feature')

    def step_module_filename(self, module_name):
        """The file name corresponding to the steps module."""

        # Importer().importFromDir('.', module_name)
        module = getsourcefile(sys.modules[module_name])
        del sys.modules[module_name]
        return module

    def test_error_message(self):
        """
        Check that the appropriate error messages are printed on failure.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/wrong_expectations.feature'

        self.assert_feature_fail(failing_feature, '--scenario-indices', '1', stream=stream)

        output = stream.getvalue()       

        feature_stack_frame = f"""
>       Then the result should be 40 on the screen

{failing_feature}:11:"""

        self.assertIn(feature_stack_frame, output)        

        step_stack_frame = """
>       assert world.result == float(result)
E       AssertionError: assert 30.0 == 40.0
"""
        self.assertIn(step_stack_frame, output)

    def test_error_message_background(self):
        """
        Check that the appropriate error messages are printed on failure in a
        step background.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/wrong_expectations_background.feature'

        self.assert_feature_fail(failing_feature, '--scenario-indices', '1', stream=stream)

        output = stream.getvalue()       

        feature_stack_frame = f"""
{failing_feature}:11: in background
    Then the result should be 40 on the screen
"""
        self.assertIn(feature_stack_frame, output)        

        step_stack_frame = """
>       assert world.result == float(result)
E       AssertionError: assert 30.0 == 40.0
"""

        self.assertIn(step_stack_frame, output)

    def test_failure_zh(self):
        """
        Test that a failing feature in Chinese fails tests.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/wrong_expectations_zh.feature'

        self.assert_feature_fail(failing_feature, stream=stream)

        # Check that the appropriate error messages were printed

        output = stream.getvalue()

        if PY3:
            feature_stack_frame = f"""
>       那么结果应该是40

{failing_feature}:12:
""".strip()

            self.assertIn(feature_stack_frame, output)
        else:
            # Cannot use non-ASCII method names in Python 2
            feature_stack_frame = f"""
{failing_feature}:12:
            """

            self.assertIn(feature_stack_frame, output)


        step_stack_frame = """
>       assert world.result == float(result)
E       AssertionError: assert 30.0 == 40.0
""".strip()

        self.assertIn(step_stack_frame, output)

    def test_step_not_found(self):
        """
        Check the behavior when a step is not defined.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/step_not_found.feature'

        self.assert_feature_fail(failing_feature, stream=stream)

        output = stream.getvalue()

        error_header = "NoDefinitionFound: " + \
            "The step r\"When I engage the warp drive\" is not defined"

        self.assertIn(error_header, output)

    def test_step_not_found_zh(self):
        """
        Check the behavior when a step is not defined with a Chinese feature.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/step_not_found_zh.feature'

        self.assert_feature_fail(failing_feature, stream=stream)

        output = stream.getvalue()

        error_header = "NoDefinitionFound: " + \
            "The step r\"当我开曲速引擎\" is not defined"

        self.assertIn(error_header, output)

    def test_background(self):
        """
        Test running a scenario with a background.
        """

        self.assert_feature_success('features/background.feature')

    def test_outlines(self):
        """
        Test a scenario with outlines.
        """

        self.assert_feature_success('features/outlines.feature')

    def test_error_message_outline(self):
        """
        Check that the appropriate error messages are printed on failure in a
        scenario outline.
        """

        stream = StreamTestWrapperIO()

        failing_feature = 'features/wrong_expectations.feature'

        self.assert_feature_fail(failing_feature, '--scenario-indices', '2', stream=stream)

        output = stream.getvalue()        
        
        feature_stack_frame = f"""
>         | 50     |

{failing_feature}:22: 
"""

        self.assertIn(feature_stack_frame, output)      

        step_stack_frame = """
>       assert world.result == float(result)
E       AssertionError: assert 30.0 == 50.0
"""
        self.assertIn(step_stack_frame, output)

    def test_python_test_skipped(self):
        """
        Test that the Python test does not get picked up.
        """

        self.assert_feature_success('tests')
   

    def test_scenario_indices(self):
        """
        Test specifying the scenario indices to run.
        """

        feature = 'features/scenario_index.feature'

        # Run a single scenario
        self.assert_feature_success(feature, '--scenario-indices', '1')
        self.assertEqual(world.all_results, [10])

        # Run multiple scenarios
        # TODO: Handling multi-valued options in Nose is tricky
        self.assert_feature_success(feature, '--scenario-indices', '1,2')
        self.assertEqual(world.all_results, [10, 20])

        # Run a scenario outline
        self.assert_feature_success(feature, '--scenario-indices', '3')
        self.assertEqual(world.all_results, [30, 40])

    def test_tags(self):
        """
        Test specifying the tags to run.
        """
        
        feature_one = 'features/withtags_one.feature'
        feature_two = 'features/withtags_two.feature'        


        # Run scenarios by tag
        self.assert_feature_success(feature_one, '-m', 'hana')
        self.assertEqual(world.all_results, [1, 11, 22])

        # Run scenarios with a tag that's not there
        self.assert_feature_success(feature_one, '-m', 'set')        

        # Run features and scenarios with the tag
        self.assert_feature_success(feature_one, feature_two, '-m', 'dul')
        self.assertEqual(world.all_results, [2, 13, 20, 200])

        # Specify a tag to exclude
        self.assert_feature_success(feature_one, '-m', 'not hana')
        self.assertEqual(world.all_results, [2, 4])

        # Specify more than one tag to run
        self.assert_feature_success(feature_one, '-m', 'hana or dul')
        self.assertEqual(world.all_results, [1, 2, 11, 22])

        # Specify more than one tag to exclude
        self.assert_feature_success(feature_one, feature_two, '-m', 'not hana and not dul')
        self.assertEqual(world.all_results, [4])

@unittest.skip("The test is no longer valid. All steps should be written/referenced in conftest.py")
class BadStepsTest(FeatureTest):
    """
    Test loading an application with an error in a step definition file.
    """

    @in_directory('tests/bad_steps_app')
    def test_parent_import_error(self):
        """
        Test the error message when a step definition file cannot be imported
        due to the parent __init__.py file not being found.
        """

        with self.assertRaises(StepDiscoveryError) as raised:
            self.run_features('features/dummy.feature')

        # The file that caused the problem should be visible
        self.assertEqual(
            str(raised.exception),
            "Cannot load step definition file: '{}'".format(
                os.path.join('features', 'steps', '__init__.py'))
        )

        # The original exception, with an unhelpful error message. Real cause:
        # features/__init__.py does not exist
        cause = raised.exception.__cause__

        self.assertIsInstance(cause, ImportError)
        # Python 3 has quotes around the module name:
        # No module named 'features'
        self.assertEqual(
            str(cause).replace('\'', ''),
            "No module named features"
        )

    @in_directory('tests/bad_steps_app_2')
    def test_normal_import_error(self):
        """
        Test the error message when a step definition file cannot be imported
        due to an error inside it.
        """

        with self.assertRaises(ValueError):
            self.run_features('features/dummy.feature')
