import setuptools
import re

VERSIONFILE = "./opendatasets/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8', errors='ignore')

setuptools.setup(
    name="opendatasets",
    version=verstr,
    author="Jovian.ml",
    author_email="hello@jovian.ml",
    description="A curated collection of datasets for data analysis & machine learning, downloadable with a single Python command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JovianML/opendatasets",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=['tqdm', 'kaggle', 'click']
)
