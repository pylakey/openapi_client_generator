import re

from setuptools import (
    find_packages,
    setup,
)

with open("README.md") as file:
    read_me_description = file.read()

with open("requirements.txt") as r:
    requirements = [i.strip() for i in r]

with open("openapi_client_generator/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

setup(
    name="openapi_client_generator",
    version=version,
    license='MIT',
    author="Pylakey",
    author_email="pylakey@protonmail.com",
    description="Async http client generator from OpenAPI schema",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['openapi_client_generator=openapi_client_generator.cli:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.9',
    include_package_data=True,
)
