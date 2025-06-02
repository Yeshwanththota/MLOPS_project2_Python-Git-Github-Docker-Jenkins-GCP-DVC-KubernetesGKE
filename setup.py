from setuptools import setup, find_packages

with open("requirements.txt") as f:	
    requirements = f.read().splitlines()

setup(
    name = "MLOPS_project2",
    version = "0.0.1",
    author = "yashwanth",
    packages= find_packages(),
    install_requires=requirements,
)