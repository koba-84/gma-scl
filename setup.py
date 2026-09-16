#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="gma-scl",
    version="0.0.1",
    description="Research code for GMA-SCL: Multi-Label Supervised Contrastive Learning",
    author="Ryoma Kobayashi",
    author_email="",
    url="https://github.com/koba-84/gma-scl",
    python_requires=">=3.12",
    install_requires=["lightning", "hydra-core"],
    packages=find_packages(),
    # use this to customize global commands available in the terminal after installing the package
    entry_points={
        "console_scripts": [
            "train_command = src.train:main",
            "eval_command = src.eval:main",
        ]
    },
)
