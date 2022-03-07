import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="fesom2_prefect",
    version="0.1.0",
    url="https://github.com/FESOM/fesom2_prefect",
    license='MIT',

    author="Paul Gierz",
    author_email="paul.gierz@awi.de",

    description="Prefect 1.0 Workflows For FESOM 2",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=["prefect==1.0", "GitPython"],
    python_requires=">=3.7,<3.10",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
