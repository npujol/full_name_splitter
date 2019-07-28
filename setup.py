import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="full_name_splitter",
    version="1.0",
    description="Divide full names into first and last names for Western names",
    url="https://github.com/npujol/full_name_splitter",
    author="Naivy Pujol Méndez",
    author_email="naivy.luna@gmail.com",
    license="MIT",
    packages=["full_name_splitter"],
    long_description=read("README"),
    zip_safe=False,
)
