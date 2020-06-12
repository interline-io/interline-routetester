from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='interline-routetester',
    version='0.3.0',
    description='Interline Route Testing Tools',
    long_description=long_description,
    url='https://github.com/interline-io/interline-routetester',
    author='Ian Rees',
    author_email='ian@interline.io',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests', 'parsedatetime', 'pytz', 'python-dateutil'], # 'locust', 
    tests_require=['nose'],
    test_suite = 'nose.collector',
    zip_safe=False,
    # Include examples.
    package_data = {
        '': ['data/*.geojson']
    },
    entry_points={
        'console_scripts': [
            'routetester=routetester.main:main',
            'routetester.starbucks=routetester.starbucks:main',
            'routetester.locust=routetester.locust:main',
            'routetester.compare=routetester.compare:main'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
    ]
)
