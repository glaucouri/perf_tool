# -*- coding: utf8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perf_tool",
    version="0.9",
    author="Glauco Uri",
    author_email="glauco@uriland.it",
    description="Performance investigaion tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/glaucouri/perf_tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
