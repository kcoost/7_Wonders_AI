from setuptools import setup
from pathlib import Path

with open(Path(__file__).parent / "requirements.txt") as file:
    install_requires = file.readlines()

setup(
    name="seven_wonders",
    version="1.0",
    description="A 7 Wonders AI",
    author="Koen Oostermeijer",
    author_email="koen@oostermeijer.net",
    packages=["seven_wonders"],
    install_requires=install_requires,
)
