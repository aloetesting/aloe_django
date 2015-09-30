"""
Setup script.
"""

__version__ = '0.0.13'

from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements, \
            open('test_requirements.txt') as test_requirements, \
            open('README.md') as readme:
        setup(
            name='aloe_django',
            version=__version__,
            description='Package for testing Django applications with Aloe',
            author='Alexey Kotlyarov',
            author_email='a@koterpillar.com',
            url='https://github.com/koterpillar/aloe_django',
            long_description=readme.read(),
            classifiers=[
                'License :: OSI Approved :: ' +
                'GNU General Public License v3 or later (GPLv3+)',
            ],

            packages=find_packages(exclude=['tests']),
            include_package_data=True,

            install_requires=requirements.readlines(),

            test_suite='tests',
            tests_require=test_requirements.readlines(),
        )
