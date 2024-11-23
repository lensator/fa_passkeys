# setup.py

from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fa_passkeys",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="A FastAPI package for WebAuthn authentication using MongoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lensator/fa_passkeys",
    packages=find_packages(),
    include_package_data=True,  # Include files specified in MANIFEST.in
    install_requires=[
        "annotated-types==0.7.0",
        "anyio==4.6.2.post1",
        "beanie==1.27.0",
        "cffi==1.17.1",
        "click==8.1.7",
        "cryptography==43.0.3",
        "dnspython==2.7.0",
        "ecdsa==0.19.0",
        "exceptiongroup==1.2.2",
        "fastapi==0.115.5",
        "fido2==1.1.3",
        "h11==0.14.0",
        "idna==3.10",
        "Jinja2==3.1.4",
        "lazy-model==0.2.0",
        "MarkupSafe==3.0.2",
        "motor==3.6.0",
        "pyasn1==0.6.1",
        "pycparser==2.22",
        "pydantic==2.10.1",
        "pydantic-settings==2.6.1",
        "pydantic_core==2.27.1",
        "pymongo==4.9.2",
        "python-dotenv==1.0.1",
        "python-jose==3.3.0",
        "rsa==4.9",
        "six==1.16.0",
        "sniffio==1.3.1",
        "starlette==0.41.3",
        "toml==0.10.2",
        "typing_extensions==4.12.2",
        "uvicorn==0.32.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.2.2",
            "flake8==6.0.0",
            "black==23.1.0",
            "httpx==0.24.1",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Update this based on your compatibility
)
