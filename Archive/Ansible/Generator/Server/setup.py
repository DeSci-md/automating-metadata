import os

from setuptools import setup, find_packages

def get_requirements():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'requirements.txt')) as f:
        return [l.strip() for l in f]

def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'version.txt')) as f:
            return f.read().strip()
    except:
        return "1.0.0"

setup(  
    name         = 'unityrest',
    version      = get_version(),
    
    packages = find_packages(),

    include_package_data = True,    
    
    tests_require = ['nose>=0.11', "coverage>=3.4"],

    test_suite = "nose.collector",

    zip_safe = False,

    install_requires = get_requirements(),
)