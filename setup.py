from setuptools import setup, find_packages

setup(
    name='CAES',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # other parameters...
)