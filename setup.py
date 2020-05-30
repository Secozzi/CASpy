from setuptools import setup, find_packages

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
    version="1.0.1",
    description="A program that provides a GUI and a CLI to a symbolic computation and computer algebra system python library, SymPy.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Secozzi/CASPy",
    author="Folke Ishii",
    author_email="folke.ishii@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'src.caspy3.resources': ['formulas.json', 'logo.png']},
    install_requires=requires(),
    entry_points={
        "console_scripts": [
            "caspy = src.caspy3.cli:main",
        ]
    }
)