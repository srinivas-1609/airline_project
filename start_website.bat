@echo off
title SkyLine Airline Reservation System
cd /d "%~dp0"

echo ================================================
echo    SkyLine Airline Reservation System
echo ================================================
echo.

echo [1/2] Starting web server on http://127.0.0.1:8765 ...
start "SkyLine-Server" cmd /k "python -m uvicorn web_api:app --host 127.0.0.1 --port 8765"

echo [2/2] Starting public internet tunnel ...
start "SkyLine-Tunnel" cmd /k "cloudflared.exe tunnel --url http://127.0.0.1:8765 --no-autoupdate"

echo.
echo Both services started in their own windows.
echo.
echo   LOCAL  :  http://127.0.0.1:8765
echo   PUBLIC :  open the "SkyLine-Tunnel" window and copy the
echo             https://xxxx.trycloudflare.com link shown there
echo.
echo Notes:
echo  - The public link changes every time you restart the tunnel.
echo  - Keep the windows open while the site should stay live.
echo  - Close both windows to stop the website.
echo.
pause
