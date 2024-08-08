from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cvtease',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'click',
        'colorama',
        'opencv-python',
        'mediapipe',
        'PySide6',  # Ensure compatibility with Python 3.7+
    ],
    entry_points={
        'console_scripts': [
            'cvtease=cvtease.cli:main',
        ],
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
