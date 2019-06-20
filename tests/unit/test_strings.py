# -*- coding: utf-8 -*-
"""
Test utilities from aloe.strings.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from aloe import strings


def test_represent_table():
    """
    Test representing a table
    """

    table = [["name", "age"], ["Gabriel Falcão", 22], ["Miguel", 19]]

    assert strings.represent_table(table) == (
        "| name           | age |\n"
        "| Gabriel Falcão | 22  |\n"
        "| Miguel         | 19  |"
    )


def test_represent_table_escapes_pipe():
    """
    Test representing a table with escaping
    """

    table = [["name", "age"], ["Gabriel | Falcão", 22], ["Miguel | Arcanjo", 19]]

    assert strings.represent_table(table) == (
        "\n".join(
            (
                r"| name              | age |",
                r"| Gabriel \| Falcão | 22  |",
                r"| Miguel \| Arcanjo | 19  |",
            )
        )
    )


def test_represent_table_allows_empty():
    """
    Test representing a table with an empty cell
    """

    table = [["name", "age"], ["Gabriel | Falcão", 22], ["Miguel | Arcanjo", ""]]

    assert strings.represent_table(table) == (
        "\n".join(
            (
                r"| name              | age |",
                r"| Gabriel \| Falcão | 22  |",
                r"| Miguel \| Arcanjo |     |",
            )
        )
    )


def test_column_width():
    """strings.column_width"""

    assert strings.get_terminal_width("あいうえお") == (10)


def test_column_width_w_number_and_char():
    """strings.column_width_w_number_and_char"""

    assert strings.get_terminal_width("%s%c" % ("4209", 0x4209)) == 6
