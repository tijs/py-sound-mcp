from setuptools import setup, find_packages

setup(
    name="mcp-sound-tool",
    version="0.1.0",
    description="An MCP server implementing a sound tool for Cursor and other MCP compatible IDEs",
    author="Tijs Teulings",
    author_email="tijs@automatique.nl",
    url="https://github.com/yourusername/mcp-sound-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=1.2.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "mcp-sound-tool=sound_tool.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={
        "sound_tool": ["sounds/*.mp3", "sounds/*.wav"],
    },
    include_package_data=True,
)