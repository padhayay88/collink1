// Test Supabase connection
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://avquikcghthqcwiscldk.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2dXFpa2NndGhocWN3aXNjbGRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUxMTYzMzIsImV4cCI6MjA3MDY5MjMzMn0.hoZzVT9SsIzXn72ECPyG37MpOgBtldO1Gp4pap61hEE';

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testConnection() {
  try {
    console.log('Testing Supabase connection...');
    
    // Test basic connection
    const { data, error } = await supabase.from('_test').select('*').limit(1);
    
    if (error) {
      console.log('Connection test result:', error.message);
    } else {
      console.log('Connection successful!');
    }
    
  } catch (err) {
    console.error('Connection failed:', err.message);
  }
}

testConnection();


