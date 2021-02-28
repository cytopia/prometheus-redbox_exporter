"""Pip configuration."""
# https://github.com/pypa/sampleproject/blob/main/setup.py

from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt", "r") as fp:
    requirements = fp.read()

setup(
    name="prometheus-redbox-exporter",
    python_requires='>3.5.2',
    version="0.1.2",
    packages=[
        "redbox",
        "redbox.config",
        "redbox.config.types",
        "redbox.request",
        "redbox.request.classes",
        "redbox.request.types",
        "redbox.types",
    ],
    entry_points={
        'console_scripts': [
            # cmd = package[.module]:func
            'redbox_exporter=redbox:main',
        ],
    },
    install_requires=requirements,
    description="Prometheus exporter that throws stuff to httpd endpoints and evaluates their response.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["prometheus", "redbox_exporter", "redbox", "blackbox", "blackbox_exporter"],
    author="cytopia",
    author_email="cytopia@everythingcli.org",
    url="https://github.com/cytopia/prometheus-redbox_exporter",
    classifiers=[
        # https://pypi.org/classifiers/
        #
        # License
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ]
)
