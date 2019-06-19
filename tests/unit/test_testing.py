# -*- coding: utf-8 -*-
"""
Test step loading.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import unittest

from tests.testing import (
    FeatureTest,
    in_directory,
)


@in_directory('tests/unit')
class FeatureTestTest(FeatureTest):
    """
    Test running features.
    """

    def test_run_good_feature_string(self):
        """
        Test running strings as features.
        """

        result = self.run_feature_string(
            """
            Feature: Empty feature

            Scenario: Empty scenario
                Given I do nothing
                Then I do nothing
            """
        )

        assert result.success, result.captured_stream.getvalue()

    def test_run_feature_string_fail(self):
        """
        Test running a failing feature string.
        """

        result = self.run_feature_string(
            """
            Feature: Empty feature

            Scenario: Empty scenario
                Given I do nothing
                Then I fail
            """
        )

        assert not result.success, result.captured_stream.getvalue()

    def test_run_feature_string_parse_error(self):
        """
        Test running a misformatted feature string.
        """

        result = self.run_feature_string(
            """
            Not a feature
            """
        )

        assert not result.success, result.captured_stream.getvalue()

    def test_run_good_feature_string_non_ascii(self):
        """
        Test running strings with non-ASCII symbols as features.
        """

        result = self.run_feature_string(
            """
            # language: zh-CN
            功能: Empty feature

            场景: Empty scenario
                当I do nothing
                那么I do nothing
            """
        )

        assert result.success, result.captured_stream.getvalue()


def relative(directory):
    """
    A directory relative to the one containing this file.
    """

    return os.path.join(os.path.dirname(__file__), directory)
