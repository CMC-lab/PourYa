from setuptools import setup, find_packages

setup(
    name="OuraDataHandler",
    version="1.0.0",
    author="Ali Mohammadi",
    author_email="1380ali.mohammadi@gmail.com",
    description="A Python library for handling Oura Ring data: fetching from API, loading from CSV, and visualising metrics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CMC-lab/OuraDataHandler",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "requests>=2.26.0",
        "ruptures>=1.1.5",
        "IPython>=8.0.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="Oura Ring data analysis API visualization health sleep",
    project_urls={
        "Documentation": "https://github.com/CMC-lab/OuraDataHandler",
        "Source": "https://github.com/CMC-lab/OuraDataHandler",
        "Tracker": "https://github.com/CMC-lab/OuraDataHandler/issues",
    },
)
