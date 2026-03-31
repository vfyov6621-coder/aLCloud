@echo off
echo ========================================
echo   aLCloud Build Script (Windows)
echo ========================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller
echo.

echo [2/3] Building application...
pyinstaller --noconfirm --onefile --windowed --name "aLCloud" main.py
echo.

echo [3/3] Done!
echo.
echo Installer: dist\aLCloud.exe
echo.
pause
