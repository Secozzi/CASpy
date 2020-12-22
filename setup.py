#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2020 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from setuptools import setup

from caspy3 import __version__


def readme():
    with open("README.md") as f:
        _readme = f.read()
    return _readme


def requires():
    with open("requirements.txt") as f:
        _requires = f.read()
    return _requires


setup(
    name="CASPy3",
    version=__version__,
    description="A program that provides both a GUI and a CLI to SymPy, a symbolic computation and computer algebra system Python library.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Secozzi/CASPy",
    author="Folke Ishii",
    author_email="folke.ishii@gmail.com",
    license="GPLv3+",
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=requires(),
    packages=["caspy3"],
    include_package_data=True,
    package_data={"caspy3": ["data/*.json"]},
    entry_points={
        "console_scripts": [
            "caspy = caspy3.cli:main",
        ]
    },
)
