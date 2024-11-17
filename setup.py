from setuptools import setup, find_packages

with open("version.txt", "r") as f:
    version = f.read().strip()

setup(
    name="Natural Disaster Scraper",
    version=version,
    packages=find_packages(),
    url="https://github.com/hangouts-chat/smart_alerts",
    license="",
    author="Enrique",
    author_email="",
    description="",
)
