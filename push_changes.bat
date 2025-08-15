@echo off
setlocal enableextensions enabledelayedexpansion

echo === Ensure Git repo ===
git rev-parse --is-inside-work-tree >NUL 2>&1
if errorlevel 1 (
  echo Initializing git repository...
  git init || goto :error
)

echo === Configure remote origin ===
set "REMOTE_URL=https://github.com/padhayay88/collink1.git"
git remote | findstr /b /c:"origin" >NUL 2>&1 && (
  git remote set-url origin %REMOTE_URL% || goto :error
) || (
  git remote add origin %REMOTE_URL% || goto :error
)

echo === Ensure on main branch ===
git rev-parse --verify main >NUL 2>&1 && (
  git checkout main || goto :error
) || (
  git checkout -B main || goto :error
)

echo === Untrack backup directories to avoid large files ===
for /D %%D in (frontend_backup_*) do (
  echo Removing from index: %%D
  git rm -r --cached --ignore-unmatch "%%D" 2>NUL
)

echo === Stage changes ===
git add -A || goto :error

echo === Commit if there are staged changes ===
git diff --cached --quiet && (
  echo No staged changes to commit.
) || (
  git commit -m "chore: sync local changes %DATE% %TIME%" || goto :error
)

echo === Fetch and rebase with origin/main ===
git fetch origin || goto :error
git pull --rebase origin main || goto :error

echo === Push to origin/main ===
git push -u origin main || goto :error

echo === Done ===
goto :eof

:error
echo.
echo ERROR: An error occurred. Aborting.
exit /b 1

