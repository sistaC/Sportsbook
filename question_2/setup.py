from setuptools import setup
import os

def parse_requirements(requirements):
    with open(requirements, encoding="utf-8") as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

#reqs = parse_requirements(os.path.dirname(os.path.realpath(__file__)) + "\\requirements.txt")
reqs = parse_requirements("requirements.txt")
setup(
   name='sportsbook',
   version='1.0',
   description='A package created to maintain sportsbook',
   author='Chidrupi Sista',
   author_email='chidrupi.sv@gmail.com',
   packages=['sportsbook'],  #same as name
   install_requires=reqs, #external packages as dependencies
   entry_points = {
        'console_scripts': ['sportsbook=sportsbook.__main__:main'],
    }
)