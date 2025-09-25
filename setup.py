from cx_Freeze import setup, Executable

# Add these options to make sure it includes the right packages
build_exe_options = {
    "packages": ["customtkinter", "webbrowser"],
    "include_files": [], # You can add image/data files here later,
     "include_msvcr": True,
}

# On Windows, the default base is 'Win32GUI'
base = "Win32GUI"

setup(
    name="AppLauncher",
    version="1.0",
    description="My Custom App Launcher",
    options={"build_exe": build_exe_options},
    executables=[Executable("launcher.py", base=base)],
)