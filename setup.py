from setuptools import setup, find_packages

setup(
    name="fred_api_project",
    version="0.1.0",
    description="A Python package for fetching and saving FRED economic data.",
    author="Kei Hendrikz",
    author_email="kei.hendrikz@8451.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyspark"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
