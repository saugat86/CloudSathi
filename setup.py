"""Setup configuration for CloudSathi CLI."""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="cloudsathi",
    version="1.0.0",
    description="Cloud cost optimization CLI for Nepal's startups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Saugat Tiwari",
    author_email="",
    url="https://github.com/saugat86/CloudSathi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cloudsathi=cli.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="cloud aws azure cost optimization cli nepal",
)
