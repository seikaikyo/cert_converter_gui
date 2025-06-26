@echo off
echo ========================================
echo Certificate Converter GUI Builder
echo By  (noreply@example.com)
echo ========================================
echo.

REM Check if GUI version exists
if not exist "cert_converter_gui.py" (
    echo ERROR: cert_converter_gui.py not found!
    echo Please make sure cert_converter_gui.py is in the same directory.
    pause
    exit /b 1
)

echo [Step 1] Checking Python and GUI support...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo OK: Python found

echo.
echo [Step 2] Installing dependencies...
echo Installing cryptography...
pip install cryptography --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install cryptography
    pause
    exit /b 1
)

echo Installing pyinstaller...
pip install pyinstaller --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install pyinstaller
    pause
    exit /b 1
)

echo Installing pillow for better GUI support...
pip install pillow --quiet

echo OK: Dependencies installed

echo.
echo [Step 3] Choose build mode:
echo 1. Single file GUI (Recommended)
echo 2. Directory mode GUI
echo.
set /p choice="Enter choice (1 or 2, default 1): "
if "%choice%"=="" set choice=1

if "%choice%"=="2" (
    set mode=--onedir
    set desc=Directory mode
) else (
    set mode=--onefile
    set desc=Single file mode
)

echo.
echo [Step 4] Building GUI executable...
echo Mode: %desc%
echo.

REM Clean old files
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul
if exist "*.spec" del "*.spec" 2>nul

echo Creating icon and resources...
REM Create a simple icon file (optional)

echo Running PyInstaller for GUI...
pyinstaller %mode% ^
    --name "CertConverter-GUI" ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --add-data "cert_converter_gui.py;." ^
    cert_converter_gui.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [Step 5] Checking output...
if "%choice%"=="2" (
    set output_path=dist\CertConverter-GUI\CertConverter-GUI.exe
) else (
    set output_path=dist\CertConverter-GUI.exe
)

if not exist "%output_path%" (
    echo ERROR: Output file not found!
    pause
    exit /b 1
)

echo.
echo ========================================
echo GUI BUILD SUCCESSFUL!
echo ========================================
echo Output: %output_path%
echo.

REM Get file size
for %%A in ("%output_path%") do set file_size=%%~zA
set /a file_size_mb=%file_size%/1024/1024
echo File size: %file_size_mb% MB

echo.
echo Creating additional files...

REM Create desktop shortcut script
(
echo @echo off
echo title Certificate Converter GUI
echo cd /d "%%~dp0"
echo start "" "CertConverter-GUI.exe"
) > "dist\Launch-GUI.bat"

REM Create GUI README
(
echo Certificate Converter GUI Tool v2.0.0
echo =====================================
echo.
echo Author:  ^(noreply@example.com^)
echo.
echo FEATURES:
echo - Beautiful graphical user interface
echo - Drag and drop support for PFX files
echo - Real-time conversion progress
echo - Support for multiple web services
echo - Built-in help and documentation
echo - Automatic output folder management
echo.
echo SUPPORTED WEB SERVICES:
echo - Nginx ^(High-performance web server^)
echo - Apache HTTP Server ^(Most popular web server^)
echo - Microsoft IIS ^(Windows web server^)
echo - HAProxy ^(Load balancer^)
echo - Traefik ^(Modern reverse proxy^)
echo - Caddy ^(Automatic HTTPS web server^)
echo.
echo HOW TO USE:
echo 1. Run CertConverter-GUI.exe
echo 2. Select or drag-drop your PFX certificate file
echo 3. Choose your target web service
echo 4. Enter PFX password if required
echo 5. Click "Start Conversion"
echo 6. Files will be generated in a service-specific folder
echo.
echo SECURITY NOTES:
echo - Private keys are converted to password-free format
echo - Suitable for web server automatic startup
echo - Please secure your private key files properly
echo - Set appropriate file permissions
echo.
echo SYSTEM REQUIREMENTS:
echo - Windows 7/8/10/11
echo - No additional software required
echo - Minimum 50MB free disk space
echo.
echo TROUBLESHOOTING:
echo - If the program doesn't start, try running as administrator
echo - Make sure your antivirus doesn't block the executable
echo - For technical support, contact: noreply@example.com
echo.
echo VERSION HISTORY:
echo v2.0.0 - GUI version with enhanced features
echo v1.0.0 - Command line version
echo.
echo Thank you for using Certificate Converter GUI!
echo.
) > "dist\GUI-README.txt"

REM Create quick start guide
(
echo QUICK START GUIDE
echo =================
echo.
echo 1. Double-click CertConverter-GUI.exe
echo 2. The beautiful GUI interface will open
echo 3. Use the drag-and-drop area to select your PFX file
echo 4. Choose your web service from the visual icons
echo 5. Enter settings and click "Start Conversion"
echo 6. Watch the progress bar and check the log
echo 7. Your converted files will be ready!
echo.
echo TIPS:
echo - Use the "Help" button for detailed information
echo - Check the log area for detailed conversion steps
echo - Enable "Open output folder" for quick access
echo - Save logs for troubleshooting if needed
echo.
echo Enjoy the professional GUI experience!
) > "dist\Quick-Start.txt"

echo OK: Additional files created

echo.
set /p test="Test run the GUI executable? (y/n): "
if /i "%test%"=="y" (
    echo Starting GUI test...
    start "" "%output_path%"
    echo GUI application should open in a new window
    timeout /t 3 /nobreak > nul
)

echo.
set /p open="Open output folder? (y/n): "
if /i "%open%"=="y" (
    start "" "dist"
)

echo.
set /p clean="Clean temporary files? (y/n, default y): "
if "%clean%"=="" set clean=y
if /i "%clean%"=="y" (
    echo Cleaning temporary files...
    if exist "build" rmdir /s /q "build" 2>nul
    if exist "CertConverter-GUI.spec" del "CertConverter-GUI.spec" 2>nul
    echo OK: Cleaned
)

echo.
echo ========================================
echo GUI BUILD COMPLETE!
echo.
echo Your professional GUI application is ready:
echo %output_path%
echo.
echo PACKAGE CONTENTS:
echo - CertConverter-GUI.exe ^(Main GUI application^)
echo - Launch-GUI.bat ^(Quick launcher^)
echo - GUI-README.txt ^(Detailed documentation^)
echo - Quick-Start.txt ^(Quick start guide^)
echo.
echo DEPLOYMENT:
echo - Copy the entire dist folder to target computers
echo - No Python installation required on target machines
echo - Works on Windows 7/8/10/11
echo - Professional GUI interface with drag-and-drop
echo.
echo FEATURES INCLUDED:
echo - Beautiful ASCII art header
echo - Drag and drop file selection
echo - Visual web service selection with icons
echo - Real-time progress tracking
echo - Comprehensive logging system
echo - Built-in help documentation
echo - Automatic output folder management
echo.
echo Thank you for using Certificate Converter GUI!
echo Contact: noreply@example.com
echo ========================================
echo.
pause