@echo off
setlocal enableextensions enabledelayedexpansion

echo === Configure remote origin (no staging) ===
set "REMOTE_URL=https://github.com/padhayay88/collink1.git"
git remote | findstr /b /c:"origin" >NUL 2>&1 && (
  git remote set-url origin %REMOTE_URL% || goto :error
) || (
  git remote add origin %REMOTE_URL% || goto :error
)

echo === Push current HEAD to origin/main ===
git push -u origin HEAD:main || goto :error

echo === Done ===
goto :eof

:error
echo.
echo ERROR: Push failed. Aborting.
exit /b 1
