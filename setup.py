from setuptools import setup

with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = "getmagnetlink",
    packages = ["getmagnetlink"],
    install_requires = ['requests', 'beautifulsoup4', 'prettytable'],
    entry_points = {
        "console_scripts": ['getmagnetlink = getmagnetlink.getmagnetlink:main']
        },
    version = "1.0.0",
    description = "Retrieves the torrent hash for the specified torrent",
    long_description = long_descr,
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    url = "https://github.com/blha303/getmagnetlink/",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Multimedia :: Sound/Audio"
        ]
    )
