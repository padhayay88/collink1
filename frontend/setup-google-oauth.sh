#!/bin/bash

echo "Setting up Google OAuth for Collink..."
echo

echo "Please follow these steps to set up Google OAuth:"
echo
echo "1. Go to https://console.cloud.google.com/"
echo "2. Create a new project or select existing one"
echo "3. Enable Google+ API and Google OAuth2 API"
echo "4. Go to Credentials > Create Credentials > OAuth 2.0 Client IDs"
echo "5. Set Application Type to 'Web application'"
echo "6. Add authorized origins: http://localhost:3000 (for development)"
echo "7. Copy the Client ID"
echo

read -p "Enter your Google OAuth Client ID: " CLIENT_ID

if [ -z "$CLIENT_ID" ]; then
    echo "No Client ID provided. Please run this script again."
    exit 1
fi

echo
echo "Creating .env.local file..."

cat > .env.local << EOF
# Google OAuth Configuration
NEXT_PUBLIC_GOOGLE_CLIENT_ID=$CLIENT_ID
EOF

echo
echo ".env.local file created successfully!"
echo
echo "Next steps:"
echo "1. Restart your development server: npm run dev"
echo "2. Test Google login on the register/login pages"
echo
echo "Note: Never commit .env.local to version control"
echo
