@echo off
echo Initializing git repository...
git init

echo Adding remote repository...
git remote add origin https://github.com/padhayay88/collink1.git

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Add chatbot feature and update dependencies"

echo Pushing to main branch...
git push -u origin main

echo Done!
pause
