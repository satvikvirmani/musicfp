import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musicfp",
    version="0.0.2",
    author="Satvik Virmani",
    author_email="virmanisatvik01@gmail.com",
    description="A terminal based media player for programmers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SatvikVirmani/musicfp",
    project_urls={
        "Bug Tracker": "https://github.com/SatvikVirmani/musicfp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio"
    ],
    package_dir={"": "src"},
    packages=["musicfp"],
    python_requires=">=3.0",
    install_requires=[
        'python-vlc'
    ],
     entry_points='''
        [console_scripts]
        musicfp=musicfp.__main__:main
    ''',
)
