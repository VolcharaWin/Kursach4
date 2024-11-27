@echo off
echo Building the project...
pyinstaller --onefile --noconsole --add-data "style.qss;." --add-data "icon.png;." --icon="icon.png" main_window.py
echo Build complete. Check the "dist" folder for the executable.
pause
