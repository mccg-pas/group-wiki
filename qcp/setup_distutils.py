import sys
from distutils.core import setup


# CHECK PYTHON IS AT LEAST PYTHON VERSION 3
if sys.hexversion < 0x3000000:
    msg = "Python version %s is unsupported, >= 3.0.0 is needed"
    print(msg % (".".join(map(str, sys.version_info[:3]))))
    exit(1)

# REWRITE SHEBANG LINE
path_to_python3 = sys.executable
lines = open("qcp/qcp", "r+").read()
with open('qcp/qcp', 'w+') as f:
    f.write(lines.replace('/bin/env python3', path_to_python3))

# CHECK NUMPY IS INSTALLED
try:
        import numpy
except ImportError:
        sys.exit("Numpy is a dependency of qcp and this python version does \n" +
                 "not seem to have numpy installed. Your options are:\n"        +
                 "1. 'pip3 install numpy' with sudo access\n"                   +
                 "2. 'pip3 install numpy' in a virtualenv of python\n"          +
                 "3. Comment out this section and procede with some functionality loss\n")

# SETUP METADATA
setup(
    # APPLICATION DETAILS
    name             = "qcp",
    version          = "2.0.0",
    author           = "Zoe L. Seeger",
    author_email     = "zoe.seeger@monash.edu",
    url              = 'https://gitlab.erc.monash.edu/zlsee3/qcp',
    license          = "LICENSE.txt",
    description      = "GAMESS, PSI4 & GAUSSIAN I/O processor",
    long_description = open("README.txt").read(),

    # MY PACKAGES TO INSTALL
    packages=["qcp"],

    # install_requires is a function of setuptools
    # not distutils - as it is more likely that
    # numpy will be installed than setuptools
    # requiring the user to have setuptools may
    # be more unhelpful than helpful
    #install_requires=['numpy', 'python>=3'],

    # CREATE bin WITH QCP IN
    scripts=['qcp/qcp'],
)
