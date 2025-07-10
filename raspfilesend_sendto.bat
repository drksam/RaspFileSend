@echo off
cd /d "C:\Users\Ronni\OneDrive\Documents\GitHub\RaspFileSend"
python "C:\Users\Ronni\OneDrive\Documents\GitHub\RaspFileSend\raspfilesend_transfer.py" %*
if errorlevel 1 (
    echo.
    echo Error occurred. Please check the configuration.
    timeout /t 5
)
pause
