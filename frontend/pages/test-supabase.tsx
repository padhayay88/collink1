import { useState } from 'react';
import { supabase } from '../lib/supabase';

export default function TestSupabase() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testSignup = async () => {
    setLoading(true);
    setResult('Testing...');
    
    try {
      console.log('Testing Supabase connection...');
      
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: 'Test User'
          }
        }
      });
      
      console.log('Signup result:', { data, error });
      
      if (error) {
        setResult(`Error: ${error.message}`);
      } else {
        setResult(`Success! Check your email: ${email}`);
        if (data.user) {
          setResult(`User created: ${data.user.id}. Check email: ${email}`);
        }
      }
    } catch (err) {
      setResult(`Exception: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-md p-6 max-w-md w-full">
        <h1 className="text-2xl font-bold mb-4">Test Supabase</h1>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="test@example.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="password123"
            />
          </div>
          
          <button
            onClick={testSignup}
            disabled={loading || !email || !password}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded disabled:opacity-50"
          >
            {loading ? 'Testing...' : 'Test Signup'}
          </button>
          
          {result && (
            <div className="mt-4 p-3 bg-gray-100 rounded">
              <pre className="text-sm">{result}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

