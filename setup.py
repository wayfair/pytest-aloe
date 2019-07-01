"""
Setup script.
"""

import io
import ast
import re
from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")
if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements, \
            open('test_requirements.txt') as test_requirements, \
            open("pytest_eucalyptus/__init__.py", "rb") as f, \
            io.open('README.md', encoding='utf-8') as readme:
        setup(
            name='pytest_eucalyptus',
            version = str(ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))),
            description='Gherkin runner compatible with Lettuce',
            author='Dennis Miasoutov',
            author_email='dmiasoutov@wayfair.com',
            url='https://github.com/wayfair/pytest-eucalyptus',
            long_description=readme.read(),
            classifiers=[
                'License :: OSI Approved :: '
                + 'GNU General Public License v3 or later (GPLv3+)',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 3',
                'Framework :: Pytest',
            ],

            packages=find_packages(exclude=['tests']),
            include_package_data=True,

            entry_points={
                'pytest11': [
                    'pytest_eucalyptus = pytest_eucalyptus.plugin',
                ],
            },

            extras_require={
                'tests_require': test_requirements.readlines(),
            },

            setup_requires=['setuptools_scm'],

            install_requires=requirements.readlines(),

            test_suite='tests',
            tests_require=test_requirements.readlines(),
        )
