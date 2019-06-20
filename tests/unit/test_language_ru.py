# -*- coding: utf-8 -*-
"""
Test Russian language parsing.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

# pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import
from builtins import *

from aloe.parser import Feature

SCENARIO = """
Сценарий: Сохранение базы курсов универитета в текстовый файл
    Допустим имеем в базе университет следующие курсы:
       | Название                | Длительность  |
       | Матан                   | 2 года        |
       | Основы программирования | 1 год         |
    Когда я сохраняю базу курсову в файл 'курсы.txt'
    Тогда в первой строке файла 'курсы.txt' строку 'Матан:2'
    И во второй строке файла 'курсы.txt' строку 'Основы программирования:1'
"""

SCENARIO_OUTLINE1 = """
Структура сценария: Заполнение пользователей в базу
    Допустим я заполняю в поле "имя" "<имя>"
    И я заполняю в поле "возраст"  "<возраст>"
    Если я сохраняю форму
    То я вижу сообщени "Студент <имя>, возраст <возраст>, успешно занесен в базу!"

Примеры:
    | имя  | возраст |
    | Вася | 22      |
    | Петя | 30      |
"""

FEATURE = """
Функционал: Деление чисел
  Поскольку деление сложный процесс и люди часто допускают ошибки
  Нужно дать им возможность делить на калькуляторе

  Сценарий: Целочисленное деление
    Допустим я беру калькулятор
    Тогда я делю делимое на делитель и получаю частное
    | делимое | делитель | частное |
    | 100     | 2        | 50      |
    | 28      | 7        | 4       |
    | 0       | 5        | 0       |
"""


def parse_scenario(string, language=None):
    """Parse a scenario, prefixing it with a feature header."""
    feature_str = """
    Функция: parse_scenario
    """
    feature_str += string
    feature = Feature.from_string(feature_str, language=language)

    return feature.scenarios[0]


def test_scenario_ru_from_string():
    """
    Language: RU -> Scenario.from_string
    """

    scenario = parse_scenario(SCENARIO, language="ru")

    assert scenario.name == "Сохранение базы курсов универитета в текстовый файл"

    assert scenario.steps[0].hashes == (
        {"Название": "Матан", "Длительность": "2 года"},
        {"Название": "Основы программирования", "Длительность": "1 год"},
    )


def test_scenario_outline1_ru_from_string():
    """
    Language: RU -> Scenario.from_string, with scenario outline, first case
    """

    scenario = parse_scenario(SCENARIO_OUTLINE1, language="ru")

    assert scenario.name == "Заполнение пользователей в базу"

    assert scenario.outlines == (
        {"имя": "Вася", "возраст": "22"},
        {"имя": "Петя", "возраст": "30"},
    )


def test_feature_ru_from_string():
    """
    Language: RU -> Feature.from_string
    """

    feature = Feature.from_string(FEATURE, language="ru")

    assert feature.name == "Деление чисел"

    assert feature.description == (
        "Поскольку деление сложный процесс и люди часто допускают ошибки\n"
        "Нужно дать им возможность делить на калькуляторе"
    )

    (scenario,) = feature.scenarios

    assert scenario.name == "Целочисленное деление"

    assert scenario.steps[-1].hashes == (
        {"делимое": "100", "делитель": "2", "частное": "50"},
        {"делимое": "28", "делитель": "7", "частное": "4"},
        {"делимое": "0", "делитель": "5", "частное": "0"},
    )
