from setuptools import setup, find_packages

setup(
    name='square_matrix_enhanced_plotter',
    version="0.1.3",
    author="Roberto Balestri",
    author_email="roberto.balestri2@unibo.it",
    description="A Python package for enhanced plotting of square matrices with zoom and interaction capabilities.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='matrix square matplotlib plot zoom interaction',
    url="https://github.com/robertobalestri/Square-Matrix-Enhanced-Plotter-Python",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "mplcursors",
        "numpy",
        "PyQT5"
    ],
    project_urls={
        "Bug Tracker": "https://github.com/robertobalestri/Square-Matrix-Enhanced-Plotter-Python",
        "Source Code": "https://github.com/robertobalestri/Square-Matrix-Enhanced-Plotter-Python",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)