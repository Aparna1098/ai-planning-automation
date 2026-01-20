from setuptools import setup, find_packages

setup(
    name="npi_agent_command_center",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "openai",
        "st-gsheets-connection",
    ],
    author="Your Name",
    description="An AI-driven NPI Command Center for supply chain orchestration.",
)