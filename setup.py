from setuptools import setup, find_packages
setup(
    name="audionet",
    version="0.2.0",
    packages=find_packages(),
    install_requires = [
        "numpy",
        "functional",
        "librosa",
        "pyworld"
    ]
)
