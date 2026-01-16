#!/usr/bin/env python
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open("trustifi/__init__.py", encoding="utf-8") as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        VERSION = match.group(1)
    else:
        raise RuntimeError("No version number found!")

setup(
    name="trustifi",
    version=VERSION,
    description="Python package for providing Google's CA Bundle.",
    long_description=open("README.md").read(),
    author="AYMENJD",
    author_email="let.me.code.safe@gmail.com",
    url="https://github.com/AYMENJD/trustifi",
    packages=[
        "trustifi",
    ],
    package_dir={"trustifi": "trustifi"},
    package_data={"trustifi": ["*.pem", "py.typed"]},
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    project_urls={
        "Source": "https://github.com/AYMENJD/trustifi",
    },
)
