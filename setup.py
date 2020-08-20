from setuptools import setup, find_packages

from caspy3 import __version__


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


def requires():
    with open('requirements.txt') as f:
        REQUIRES = f.read()
    return REQUIRES


setup(
    name="CASPy3",
    version=__version__,
    description="A program that provides a GUI and a CLI to a symbolic computation and computer algebra system python library, SymPy.",
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
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    entry_points={
        "console_scripts": [
            "caspy = caspy3.cli:main",
        ]
    }
)
