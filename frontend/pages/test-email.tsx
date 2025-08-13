import { useState } from 'react';
import { supabase } from '../lib/supabase';

export default function TestEmail() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testEmail = async () => {
    setLoading(true);
    setResult('Testing email...');
    
    try {
      // Test 1: Check if user exists
      const { data: existingUser } = await supabase.auth.admin.getUserByEmail(email);
      
      if (existingUser.user) {
        setResult(`User already exists: ${existingUser.user.id}`);
        return;
      }

      // Test 2: Try to sign up
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: 'Test User'
          }
        }
      });
      
      if (error) {
        setResult(`Error: ${error.message}`);
        return;
      }

      if (data.user) {
        setResult(`✅ User created: ${data.user.id}\n📧 Email should be sent to: ${email}\n\nCheck your email and spam folder.`);
        
        // Test 3: Check user status after a delay
        setTimeout(async () => {
          const { data: userData } = await supabase.auth.admin.getUserById(data.user.id);
          if (userData.user) {
            setResult(prev => prev + `\n\nUser status: ${userData.user.email_confirmed_at ? 'Email confirmed' : 'Email not confirmed'}`);
          }
        }, 2000);
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
        <h1 className="text-2xl font-bold mb-4">Email Test</h1>
        
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
            onClick={testEmail}
            disabled={loading || !email || !password}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded disabled:opacity-50"
          >
            {loading ? 'Testing...' : 'Test Email Sending'}
          </button>
          
          {result && (
            <div className="mt-4 p-3 bg-gray-100 rounded">
              <pre className="text-sm whitespace-pre-wrap">{result}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

