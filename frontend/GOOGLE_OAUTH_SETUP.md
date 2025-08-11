# Google OAuth Setup Guide

To enable Google login functionality in your Collink application, follow these steps:

## 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Google+ API
   - Google OAuth2 API

## 2. Create OAuth 2.0 Credentials

1. Go to **Credentials** in the left sidebar
2. Click **Create Credentials** → **OAuth 2.0 Client IDs**
3. Set **Application Type** to "Web application"
4. Add **Authorized JavaScript origins**:
   - `http://localhost:3000` (for development)
   - `https://yourdomain.com` (for production)
5. Click **Create**
6. Copy the **Client ID**

## 3. Environment Configuration

Create a `.env.local` file in your `frontend` directory:

```bash
# Google OAuth Configuration
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-actual-client-id-here
```

Replace `your-actual-client-id-here` with the Client ID you copied from Google Cloud Console.

## 4. Restart Development Server

After adding the environment variable, restart your Next.js development server:

```bash
npm run dev
```

## 5. Test Google Login

1. Navigate to `/register` page
2. Click the "Continue with Google" button
3. Complete Google OAuth flow
4. You should be redirected to the home page after successful login

## Security Notes

- Never commit your `.env.local` file to version control
- The `NEXT_PUBLIC_` prefix makes the variable available in the browser
- For production, ensure you have proper domain verification in Google Cloud Console

## Troubleshooting

- **"Invalid Client ID" error**: Double-check your Client ID in `.env.local`
- **"Origin not allowed" error**: Verify your domain is in the authorized origins list
- **API not enabled**: Make sure Google+ API and Google OAuth2 API are enabled

## Additional Features

The current implementation includes:
- ✅ Phone number registration with country codes
- ✅ Email registration
- ✅ Google OAuth integration
- ✅ Form validation
- ✅ Password strength requirements
- ✅ Terms and conditions agreement
- ✅ Responsive design with animations
