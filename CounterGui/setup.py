import sys
import cx_Freeze

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


executables= [cx_Freeze.Executable("app.py")]

cx_Freeze.setup(name="POs Counter", 
            options={
                    "build_exe": {
                            "packages": ["tkinter"],
                            "include_files": ["./icons/"]
                        }
                },
            version="0.0.1",
            executables=executables
        )
