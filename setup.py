from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="renai",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="RenAI - Intelligent AI Companion with MLOps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/RenAI-Companion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=6.0.0",
        ],
        "ml": [
            "mlflow>=1.30.0",
            "dvc>=2.26.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "renai-train=ml_pipeline.src.train_pipeline:main",
            "renai-api=backend.app.main:start",
            "renai-dash=dashboard.app:main",
        ],
    },
)