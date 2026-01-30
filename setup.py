from setuptools import setup, find_packages

setup(
    name="npi_control_tower",
    version="1.0.0",
    description="Agentic Supply Chain Risk Management System",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
    ],
    python_requires=">=3.12",
)
