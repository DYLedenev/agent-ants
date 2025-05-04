from setuptools import setup, find_packages

setup(
    name="agent_ants",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "rich",
        "pytest"
    ],
)