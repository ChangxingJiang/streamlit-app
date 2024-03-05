from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding="UTF-8") as file:
    long_description = file.read()

setup(
    name="streamlit-app",  # 包名
    version="0.0.1",
    description="A applet to use streamlit objectification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="changxing",
    author_email="1278729001@qq.com",
    url="",
    install_requires=["streamlit==1.31.0"],
    license="MIT License",
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries"
    ]
)
