@echo off
echo 🚀 Setting up Collink Frontend...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

echo 🔧 Creating environment file...
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

echo ✅ Environment file created!

echo 🎉 Frontend setup complete!
echo.
echo To start the development server:
echo   npm run dev
echo.
echo Make sure the backend is running on port 8000:
echo   python main.py
echo.
echo Then open http://localhost:3000 in your browser
pause 