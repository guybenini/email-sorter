from cx_Freeze import setup, Executable
import os

# Define additional files to include
include_files = [
    ('smtp_settings.py', '.'),  # Include smtp_settings.py in the same directory as the executable
    ('email.png', '.'),         # Include an icon file if you have one
]

# Define build options
build_options = {
    'packages': ['requests', 'bs4', 'email_validator', 'tkinter'],  # Include necessary packages
    'excludes': [],                                                # List of packages to exclude if any
    'include_files': include_files,
    'optimize': 2,                                                 # Optimization level
}

# Define the executables
executables = [
    Executable(
        'main.py',                # Your main script
        base=None,                # Set to "Win32GUI" for GUI apps, None for console apps
        target_name='DataSpyderEmailSuite.exe',  # Name of the executable
        icon='email.png'          # Path to your icon file (optional)
    )
]

# Setup function
setup(
    name='DataSpyderEmailSuite',
    version='1.0',
    description='A tool for email scraping and validation',
    options={'build_exe': build_options},
    executables=executables
)
