import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('theGUI.py', base=base)
]

setup(name='simple_Tkinter',
      version='0.1',
      description='blaaaaa',
      executables=executables,
      options={"build_exe": {"replace_paths": [("*", "")],
                             "zip_include_packages": ["*"],
                             "zip_exclude_packages": []}})

#setup(name="test_sqlite3",
      #version="0.3",
      #description="cx_Freeze script to test sqlite3",
      #executables=[Executable("test_sqlite3.py")],
      #options={"build_exe": {"excludes": ["tkinter"],
                             #"replace_paths": [("*", "")],
                             #"zip_include_packages": ["*"],
                            # "zip_exclude_packages": []}})