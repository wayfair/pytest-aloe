"""
Setup script.
"""

import io
from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements, \
            open('test_requirements.txt') as test_requirements, \
            io.open('README.md', encoding='utf-8') as readme:
        setup(
            name='pytest-aloe',
            use_scm_version=True,
            description='Gherkin runner compatible with Lettuce',
            author='Dennis Miasoutov',
            author_email='dmiasoutov@wayfair.com',
            url='https://github.com/wayfair/pytest-aloe',
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
                    'pytest-aloe = pytest_aloe.plugin',
                ],
            },

            setup_requires=['setuptools_scm'],

            install_requires=requirements.readlines(),

            test_suite='tests',
            tests_require=test_requirements.readlines(),
        )
