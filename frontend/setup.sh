#!/bin/bash

echo "🚀 Setting up Collink Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "✅ Dependencies installed successfully!"

echo "🔧 Creating environment file..."
cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000
EOL

echo "✅ Environment file created!"

echo "🎉 Frontend setup complete!"
echo ""
echo "To start the development server:"
echo "  npm run dev"
echo ""
echo "Make sure the backend is running on port 8000:"
echo "  python main.py"
echo ""
echo "Then open http://localhost:3000 in your browser" 