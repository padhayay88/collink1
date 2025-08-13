import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '../../lib/supabase';
import { useAuth } from '../../lib/auth';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, Loader } from 'lucide-react';

export default function AuthCallback() {
  const router = useRouter();
  const { login } = useAuth();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Verifying your email...');

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        // Get the hash fragment from the URL
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        
        // Check for error parameters
        const error = params.get('error');
        const errorDescription = params.get('error_description');
        
        if (error) {
          console.error('Auth error:', error, errorDescription);
          setStatus('error');
          setMessage(errorDescription || 'Authentication failed. Please try again.');
          return;
        }

        // Handle the auth callback
        const { data, error: authError } = await supabase.auth.getSession();
        
        if (authError) {
          console.error('Auth callback error:', authError);
          setStatus('error');
          setMessage('Failed to verify your email. Please try again.');
          return;
        }

        if (data.session?.user) {
          // User is authenticated
          const userData = {
            id: data.session.user.id,
            name: data.session.user.user_metadata?.full_name || data.session.user.email?.split('@')[0] || 'User',
            email: data.session.user.email,
          };
          
          login(userData);
          setStatus('success');
          setMessage('Email verified successfully! Welcome to Collink!');
          
          // Redirect to home page after a short delay
          setTimeout(() => {
            router.push('/');
          }, 2000);
        } else {
          setStatus('error');
          setMessage('No user session found. Please try registering again.');
        }
        
      } catch (error) {
        console.error('Auth callback error:', error);
        setStatus('error');
        setMessage('An unexpected error occurred. Please try again.');
      }
    };

    handleAuthCallback();
  }, [router, login]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center"
      >
        {status === 'loading' && (
          <div className="space-y-4">
            <Loader className="w-12 h-12 text-blue-600 animate-spin mx-auto" />
            <h2 className="text-xl font-semibold text-gray-900">Verifying Email</h2>
            <p className="text-gray-600">{message}</p>
          </div>
        )}

        {status === 'success' && (
          <div className="space-y-4">
            <CheckCircle className="w-12 h-12 text-green-600 mx-auto" />
            <h2 className="text-xl font-semibold text-gray-900">Success!</h2>
            <p className="text-gray-600">{message}</p>
            <p className="text-sm text-gray-500">Redirecting to home page...</p>
          </div>
        )}

        {status === 'error' && (
          <div className="space-y-4">
            <XCircle className="w-12 h-12 text-red-600 mx-auto" />
            <h2 className="text-xl font-semibold text-gray-900">Verification Failed</h2>
            <p className="text-gray-600">{message}</p>
            <div className="space-y-2">
              <button
                onClick={() => router.push('/register')}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Try Registering Again
              </button>
              <button
                onClick={() => router.push('/')}
                className="w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Go to Home
              </button>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

