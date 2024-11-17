from setuptools import setup, find_packages

with open("version.txt", "r") as f:
    version = f.read().strip()

setup(
    name="Twitter Scraper",
    version=version,
    packages=find_packages(),
    url="https://github.com/hangouts-chat/twitter-scraper",
    license="",
    author="Enrique",
    author_email="",
    description="",
)
