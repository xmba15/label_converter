#!/usr/bin/env python
from setuptools import setup, find_packages
import os
from io import open


_PARENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
_LONG_DESCRIPTION = open(os.path.join(_PARENT_DIRECTORY, "README.md"), encoding="utf-8").read()
_INSTALL_REQUIRES = open(os.path.join(_PARENT_DIRECTORY, "requirements.txt")).read().splitlines()


def main():
    setup(
        name="label_converter",
        version="0.1.0",
        description="utility package to convert back and forth among popular dataset label formats",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author="xmba15",
        url="https://github.com/xmba15/label_converter.git",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
        packages=find_packages(exclude=["tests"]),
        install_requires=_INSTALL_REQUIRES,
        entry_points={"console_scripts": ["label_converter=label_converter.__main__:main"]},
    )


if __name__ == "__main__":
    main()
