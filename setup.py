import os

from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))
about = {}
version = os.path.join(HERE, "hier_client", "__version__.py")
with open(version, "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["requests", 'keyring']
setup(
    name=about["__title__"],
    version=about["__version__"],
    install_requires=requirements,
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    packages=["hier_client"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["hier = hier_client.client:run"]},
)
