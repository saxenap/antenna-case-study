from setuptools import setup, find_packages

setup(
    name         = 'antenna',
    version      = '1.0',
    packages=find_packages(exclude=('tests')),
)