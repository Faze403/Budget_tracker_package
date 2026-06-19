from setuptools import find_packages, setup


setup(
    name="budget-tracker",
    version="0.1.0",
    description="Track income, expenses, and monthly budget summaries.",
    author="PARK SEOJIN",
    author_email="cockatoo@kku.ac.kr",
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[],
    python_requires=">=3.10",
)
