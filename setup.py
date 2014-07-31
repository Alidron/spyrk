import sys
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from setuptools.command.test import test as TestCommand
from codecs import open  # To use a consistent encoding
from os import path

# From https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(path.join(*paths), 'r') as f:
        return f.read()
        
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None
        
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        
    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='spyrk',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.0.3',

    description='Python module for Spark devices',
    long_description=(read('README.rst') + '\n\n' +
                      read('AUTHORS.rst') + '\n\n' +
                      read('CHANGELOG.rst')),

    # The project's main homepage.
    url='https://github.com/Alidron/spyrk',

    # Author details
    author='Axel Voitier',
    author_email='axel.voitier@gmail.com',

    # Choose your license
    license='LGPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Topic :: Home Automation',
        'Topic :: Software Development :: Embedded Systems',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='spark cloud core arduino api embedded',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    py_modules=['spyrk'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=['hammock'],
    
    tests_require = ['pytest'],
    cmdclass = { 'test': PyTest },
)
