from setuptools import setup, find_packages
from pathlib import Path

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Adding the `install.sh` script to the package data
setup(
    name='cvtease',
    version='0.1.17',
    packages=find_packages(),
    install_requires=[
        'click',
        'colorama',
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'cvtease=cvtease.cli:main',
        ],
    },
    include_package_data=True,  # Include package data files
    package_data={
        '': ['install.sh'],  # Include `install.sh` in the package
    },
    author='w3cdpass',
    author_email='kupasva663@gmail.com',
    description='A CLI tool for computer vision that is under development. Includes a space shooter game using ASCII art.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/w3cdpass/cvtease',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
