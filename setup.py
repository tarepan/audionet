from setuptools import setup, find_packages
setup(
    name="audionet",
    version="0.1.0",
    packages=find_packages(),
    install_requires = [
        "functional",
        "librosa",
        "pyworld"
    ]
)
