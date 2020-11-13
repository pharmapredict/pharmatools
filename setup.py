from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name="pharmatools",
    version="1.0",
    description="helper functions for the Le Wagon PharmaPredict team",
    packages=find_packages(),
    test_suite="tests",
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    scripts=["scripts/pharmatools-run"],
    zip_safe=False,
)
