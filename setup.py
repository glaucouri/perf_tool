# -*- coding: utf8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perf_tool",
    version="0.9.1",
    author="Glauco Uri",
    author_email="glauco@uriland.it",
    description="Performance investigation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/glaucouri/perf_tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
