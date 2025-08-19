import type { AppProps } from 'next/app'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from '../lib/auth'
import dynamic from 'next/dynamic'
import '../styles/globals.css'
import { ChakraProvider } from '@chakra-ui/react'

const queryClient = new QueryClient()

// Google OAuth Client ID - Replace with your actual Google OAuth Client ID
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "your-google-client-id-here"

export default function App({ Component, pageProps }: AppProps) {
  const ChatbotWidget = dynamic(() => import('../components/Chatbot/ChatbotWidget'), { ssr: false })
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <AuthProvider>
            <Component {...pageProps} />
            <ChatbotWidget />
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
        </ChakraProvider>
      </QueryClientProvider>
    </GoogleOAuthProvider>
  )
}