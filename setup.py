import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruben-snake-cmd",
    version="0.2.3",
    author="Ruben Dougall",
    author_email="info.ruebz999@gmail.com",
    description="Command-line version of the classic Snake game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruben9922/snake-cmd",
    keywords="snake game console command-line curses",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console :: Curses",
        "Natural Language :: English",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['ruben-snake-cmd=snake_cmd:main'],
    },
    py_modules=['snake_cmd'],
    install_requires=["numpy", "ruben-curses-game-utilities"],
)
