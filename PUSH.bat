@echo off
cd /d "%~dp0"
git add .
git commit -m "Aktualizacja %date% %time%"
git push origin main
echo.
echo Gotowe\! Strona zaktualizowana.
pause
