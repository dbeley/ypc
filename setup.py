import setuptools
import youtube_playlist_converter

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="youtube_playlist_converter",
        version=youtube_playlist_converter.__version__,
        author="dbeley",
        author_email="dbeley@protonmail.com",
        description="Convert spotify/deezer/text playlists to youtube urls or audio/video files",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dbeley/youtube_playlist_converter",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "ypc=youtube_playlist_converter.__main__:main"
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
            ],
        install_requires=[
            'requests',
            'spotipy',
            'pandas',
            'bs4',
            'youtube-dl',
            'lxml',
            ]
        )
