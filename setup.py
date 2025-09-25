"""
Setup configuration for App Launcher
Handles both development installation and executable creation
"""

import sys
from cx_Freeze import setup, Executable
from pathlib import Path

# Read version from a version file
VERSION = "1.0.0"

# Read long description from README.md
readme_file = Path(__file__).parent / "README.md"
try:
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A customizable application launcher with drag-and-drop interface"

# Dependencies
required_packages = [
    "customtkinter>=5.2.0",
    "keyboard>=0.13.5",
]

# Build options for cx_Freeze
build_exe_options = {
    "packages": [
        "customtkinter",
        "keyboard",
        "webbrowser",
        "json",
        "logging",
        "pathlib",
        "typing",
    ],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": [
        "README.md",
        "LICENSE",
    ],
    "include_msvcr": True,
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable configuration
executable = Executable(
    script="launcher.py",
    base=base,
    target_name="AppLauncher",
    icon="icon.ico",  # You'll need to create this
    shortcut_name="App Launcher",
    shortcut_dir="DesktopFolder",
    copyright="Copyright © 2025 ApexDazza",
)

setup(
    name="app-launcher",
    version=VERSION,
    description="A customizable application launcher with drag-and-drop interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ApexDazza",
    author_email="your.email@example.com",  # Update this
    url="https://github.com/ApexDazza/app-launcher",
    packages=["app_launcher"],
    package_dir={"app_launcher": "."},
    python_requires=">=3.8",
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "applauncher=launcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Desktop Environment",
    ],
    options={
        "build_exe": build_exe_options,
    },
    executables=[executable],
)

setup(
    name="AppLauncher",
    version="1.0",
    description="My Custom App Launcher",
    options={"build_exe": build_exe_options},
    executables=[Executable("launcher.py", base=base)],
)