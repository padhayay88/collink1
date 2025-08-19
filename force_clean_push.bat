@echo off
setlocal enableextensions

echo === Remove backups from history ===
git filter-branch --force --index-filter "git rm -r --cached --ignore-unmatch --quiet frontend_backup_20250815_223455" --prune-empty --tag-name-filter cat -- --all || goto :error

echo === Cleanup refs ===
for /f "delims=" %%R in ('git for-each-ref --format="%%(refname)" refs/original/') do git update-ref -d "%%R"
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo === Force push ===
git push --force origin main || goto :error

echo === Done ===
exit /b 0

:error
echo ERROR: Failed. Check previous output for details.
exit /b 1
