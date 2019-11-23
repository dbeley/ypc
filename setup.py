import setuptools
import ypc

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ypc",
    version=ypc.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Convert spotify/deezer/text playlists to youtube urls or audio/video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/ypc",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["ypc=ypc.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "requests",
        "spotipy",
        "pandas",
        "beautifulsoup4",
        "youtube-dl",
        "lxml",
        "tqdm",
        "itunespy",
    ],
)
