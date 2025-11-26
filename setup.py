from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="user-creation-script",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A script to create users from CSV files via API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/user-creation-script",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "flake8>=6.1.0",
            "black>=23.12.1",
            "bandit>=1.7.5",
            "safety>=2.3.5",
            "responses>=0.24.1",
        ],
    },
)