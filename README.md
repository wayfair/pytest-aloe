# Eucalyptus - BDD plugin for Pytest
> A nice fork of [Aloe](https://github.com/aloetesting/aloe). 
Migrated from Nose to Pytest.

[![pypi][pypi]][pypi-url]
[![pypi-versions][pypi-versions]][pypi-url]
[![builds][builds]][builds-url]
[![docs][docs]][docs-url]
[![coverage][cover]][cover-url]

**pytest-eucalyptus** has been built to feature the best of both worlds: 
- [Aloe](https://github.com/aloetesting/aloe) which implements great infrastructure and uses the original Gherkin parser.
- [pytest-bdd](https://github.com/pytest-dev/pytest-bdd) does not require a separate runner and benefits from the power and flexibility of Pytest.

## Quick Start

1. Create new module and add empty `__init__.py`.

2. Install Pytest and Eucalyptus:

    ```sh
    pip install pytest pytest-eucalyptus
    ```

3. Let's assume we are testing the following implementation of `calculator.py`:

    ```py

        def add(*numbers):
            return sum(numbers)
    ```

4. Write your first feature ``tests/calculator.feature``:

    ```feature
        Feature: Add up numbers

        As a mathematically challenged user
        I want to add numbers
        So that I know the total

        Scenario: Add two numbers
            Given I have entered 50 into the calculator
            And I have entered 30 into the calculator
            When I press add
            Then the result should be 80 on the screen
    ```

5. Add the definitions in ``tests/conftest.py``:

    ```py
        from calculator import add
        from pytest_eucalyptus import before, step, world


        @before.each_example
        def clear(*args):
            """Reset the calculator state before each scenario."""
            world.numbers = []
            world.result = 0


        @step(r'I have entered (\d+) into the calculator')
        def enter_number(self, number):
            world.numbers.append(float(number))


        @step(r'I press add')
        def press_add(self):
            world.result = add(*world.numbers)


        @step(r'The result should be (\d+) on the screen')
        def assert_result(self, result):
            assert world.result == float(result)
    ```

6. Run the code

```sh
    $ pytest
```

```
============================= test session starts ==============================
platform darwin -- Python 3.7.3, pytest-4.6.3, py-1.8.0, pluggy-0.12.0
rootdir: /Users/eucalyptus-user/src/test
plugins: eucalyptus-0.3.0
collected 1 item                                                               

calculator.feature .                                                     [100%]

=========================== 1 passed in 0.01 seconds ===========================

```

## Documentation

Please find more docs [here](https://eucalyptus.readthedocs.io/).

## License

Pytest-Eucalyptus is licensed under the Apache License 2.0 – see the [LICENSE.md](https://github.com/wayfair/pytest-eucalyptus/blob/master/LICENSE) for specific details.

[pypi]: https://img.shields.io/pypi/v/pytest-eucalyptus.svg
[pypi-versions]: https://img.shields.io/pypi/pyversions/pytest-eucalyptus.svg
[pypi-url]: https://pypi.org/project/pytest-eucalyptus

[builds]: https://travis-ci.org/wayfair/pytest-eucalyptus.svg?branch=master
[builds-url]: https://travis-ci.org/wayfair/pytest-eucalyptus

[cover]: https://codecov.io/gh/wayfair/pytest-eucalyptus/branch/master/graph/badge.svg
[cover-url]: https://codecov.io/gh/wayfair/pytest-eucalyptus

[docs]: https://readthedocs.org/projects/eucalyptus/badge/?version=latest
[docs-url]: https://eucalyptus.readthedocs.io/?badge=latest