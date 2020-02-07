from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="TapTargetView",
    version="0.1.2",
    packages=["taptargetview"],
    scripts=["taptargetview/taptargetview.py"],
    package_data={"taptargetview": ["*.py"],},
    # metadata to display on PyPI
    author="Shashi Ranjan",
    author_email="shashiranjankv@gmail.com",
    description="Attempt to mimic Android's TapTargetView using Kivy and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Kivy Python TapTargetView",
    url="https://github.com/shashi278/TapTargetView",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["kivy",],
    python_requires=">=3.6",
)
