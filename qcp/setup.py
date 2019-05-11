import os, sys
from setuptools import setup, find_packages

# SETUP METADATA, USES setuptools.setup and .find_packages
setup(
    # APPLICATION DETAILS
    name             = "qcp",
    version          = "2.0",
    author           = "Zoe L. Seeger",
    author_email     = "zoe.seeger@monash.edu",
    url              = "https://gitlab.erc.monash.edu/zlsee3/qcp",
    license          = "LICENSE.txt",
    description      = "GAMESS, PSI4 & GAUSSIAN I/O processor",
    long_description = open("README.txt").read(),

    # FOR SETUPTOOLS
    packages=find_packages(),

    # FILES TO INCLUDE : IF SET TO TRUE WILL READ FROM MANIFEST.in
    include_package_data=True,

    # SYSTEM AND PIP METADATA
    classifiers=[
        # only compatible with Python 3
        "Programming Language :: Python :: 3",
        # licensed under GNU GENERAL PUBLIC LICENSE
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # OS-independent
        "Operating System :: OS Independent",
        # TAGS
        "Topic :: Scientific/Engineering :: Chemistry",
        "Natural Language :: English",
        "Development Status :: 5 - Production/Stable"
        ],

    # REQUIRES PYTHON VERSION
    python_requires='>=3.0',

    # DEPENDENCIES TO INSTALL IF NOT AVAILABLE
    install_requires=[
        "numpy"
        ],

    entry_points={
        "console_scripts" : [
            "qcp = qcp.__main__:main"
            ],
        "gui_scripts" : [
            ]
        },

)
