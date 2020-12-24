#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()


import csvwrangle as SETTINGS

install_requirements = [
    "Click>=7.0",
    "pandas>=1.1",
]

setup_requirements = [
    "pytest-runner",
]
test_requirements = [
    "coverage>=5",
    "pytest>=5",
]

setup(
    name="csvwrangle",
    version=SETTINGS.__version__,
    author=SETTINGS.__author__,
    author_email=SETTINGS.__author_email__,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Pytest",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    description="Wrangle CSV data with pandas from the command-line",
    entry_points={
        "console_scripts": [
            "csvwrangle=csvwrangle.cli:main",
            "cwr=csvwrangle.cli:main",

        ],
    },
    extras_require={
        "dev": [
            "black",
            "tox>=3.14",
            "twine>=3",
        ],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-autobuild",
            "vega_datasets",
            "watchdog",
        ],
        "tests": test_requirements,
    },
    install_requires=install_requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="csvwrangle",
    packages=find_packages(include=["csvwrangle", "csvwrangle.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    # tests_require=test_requirements,
    url="https://github.com/dannguyen/csvwrangle",
    zip_safe=False,
)
