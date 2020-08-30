from setuptools import setup

from caspy3 import __version__


def readme():
    with open('README.md') as f:
        _readme = f.read()
    return _readme


def requires():
    with open('requirements.txt') as f:
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
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=requires(),
    packages=["caspy3"],
    include_package_data=True,
    package_data={"caspy3": ["data/*.json"]},
    entry_points={
        "console_scripts": [
            "caspy = caspy3.cli:main",
        ]
    }
)
