# Supabase Setup Guide for Collink

## 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in to your account
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - **Name**: `collink-auth` (or any name you prefer)
   - **Database Password**: Create a strong password
   - **Region**: Choose the closest region to your users
6. Click "Create new project"

## 2. Get Your Project Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **Anon public key** (starts with `eyJ...`)

## 3. Configure Environment Variables

1. Copy the `env.example` file to `.env.local`:
   ```bash
   cp env.example .env.local
   ```

2. Edit `.env.local` and replace the placeholder values:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## 4. Configure Authentication Settings

1. In your Supabase dashboard, go to **Authentication** → **Settings**
2. Configure the following:

### Email Templates
- Go to **Email Templates** tab
- Customize the "Confirm signup" template if desired
- The default template will work fine

### Site URL
- Set **Site URL** to: `http://localhost:3000` (for development)
- For production, set it to your actual domain

### Redirect URLs
- Add these redirect URLs:
  - `http://localhost:3000/auth/callback`
  - `http://localhost:3000/register`
  - `http://localhost:3000/login`

## 5. Enable Email Confirmation

1. In **Authentication** → **Settings** → **General**
2. Make sure **Enable email confirmations** is checked
3. Set **Secure email change** to enabled (recommended)

## 6. Test the Setup

1. Start your development server:
   ```bash
   npm run dev
   ```

2. Go to `http://localhost:3000/register`
3. Try creating an account with a real email address
4. Check your email for the confirmation link
5. Click the link or use the authentication code feature

## 7. Production Deployment

When deploying to production:

1. Update your environment variables with production URLs
2. Set the **Site URL** in Supabase to your production domain
3. Add your production domain to **Redirect URLs**
4. Consider enabling additional security features like:
   - Rate limiting
   - CAPTCHA
   - Phone number verification

## Troubleshooting

### Common Issues

1. **"Supabase configuration is missing"**
   - Make sure you've created `.env.local` with the correct values
   - Restart your development server after adding environment variables

2. **Email not received**
   - Check your spam folder
   - Verify the email address is correct
   - Check Supabase logs in the dashboard

3. **Authentication code not working**
   - The current implementation simulates verification
   - For real verification, you'll need to implement Supabase's email confirmation flow

### Support

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [Next.js with Supabase](https://supabase.com/docs/guides/getting-started/tutorials/with-nextjs)
