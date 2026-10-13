@echo off
cd /d "%~dp0"
python -c "import tkinter, keyboard, numpy, sounddevice, pystray; from PIL import Image, ImageTk" >nul 2>&1
if errorlevel 1 (
  echo Installing the small UI and tray dependencies. Please wait...
  python -m pip install keyboard numpy sounddevice pystray pillow
  if errorlevel 1 (
    echo Installation failed. Please share the error above.
    pause
    exit /b 1
  )
)
python -c "import sys, subprocess; from pathlib import Path; app=Path(sys.executable).with_name('pythonw.exe'); assert app.is_file(), 'Cannot find pythonw.exe alongside Python'; subprocess.Popen([str(app), str(Path.cwd() / 'voice_typing.pyw')], creationflags=0x08000000)"
if errorlevel 1 (
  echo LumaScribe could not open. Please share the error above.
  pause
)
