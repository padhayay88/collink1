import type { AppProps } from 'next/app'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from '../lib/auth'
import '../styles/globals.css'

const queryClient = new QueryClient()

// Google OAuth Client ID - Replace with your actual Google OAuth Client ID
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "your-google-client-id-here"

export default function App({ Component, pageProps }: AppProps) {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Component {...pageProps} />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </AuthProvider>
      </QueryClientProvider>
    </GoogleOAuthProvider>
  )
} 