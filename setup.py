import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pylint-plus",
    version="0.0.1",
    description="Pylint extension with good practices and code smell detection",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/leandroltavares/pylint-plus",
    author="Leandro Luciani Tavares",
    author_email="leandro.ltavares@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    packages=["pylint_plus"],
    include_package_data=True,
    install_requires=[
        'pylint>=2.8.0',
    ],
    keywords='pylint linting code smells extensions',
)