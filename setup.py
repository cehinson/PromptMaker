from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptmaker",
    version="0.1.0",
    author="Charles Hinson",
    author_email="cehinso17@gmail.com",
    description="A tool to analyze project files and generate structured prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cehinson/PromptMaker",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "promptmaker=promptmaker.main:main",
        ],
    },
)
