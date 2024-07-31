from setuptools import setup, find_packages

setup(
    name='funny-face',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'funny-face=funny_face.cli:main',
        ],
    },
    author='Kupasva',
    author_email='kupasva663@gmail.com',
    description='A CLI tool for computer vision that is under development. Includes a space shooter game using ASCII art.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/w3cdpass/funny-face',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
