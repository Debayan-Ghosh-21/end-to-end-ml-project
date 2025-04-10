
from setuptools import setup, find_packages

def get_requirements(filepath: str):
    requirements=open(filepath).read().splitlines()

    if '-e.' in requirements:
        requirements.remove('-e.')
        
    return requirements

setup(
name='Mlproject',
version='0.0.1',
author='Debayan',
author_email='gdebayan185@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)

