# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (setup.py) is part of AsyncSpotify which is released under MIT.                       #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async-spotify",
    packages=setuptools.find_packages(),
    version="0.2.0",
    author="HuiiBuh",
    author_email="nhaderer1@gmail.com",
    description="An async spotify api client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuiiBuh/AsyncSpotify",
    keywords=["Spotify", "Async", "API", "Wrapper", "AioHttp"],
    install_requires=["aiohttp>=3.6.2", "aiodns>=2.0.0"],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
