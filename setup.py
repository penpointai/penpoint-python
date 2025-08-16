from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="penpoint",
    version="0.1.0",
    author="Penpoint",
    author_email="support@penpoint.ai",
    description="Official Python client library for the Penpoint API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/penpoint/penpoint-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "typing-extensions>=3.7.4;python_version<'3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    keywords="penpoint, api, client, document, reference, search",
    project_urls={
        "Bug Reports": "https://github.com/penpoint/penpoint-python/issues",
        "Source": "https://github.com/penpoint/penpoint-python",
        "Documentation": "https://penpoint-python.readthedocs.io/",
    },
)
