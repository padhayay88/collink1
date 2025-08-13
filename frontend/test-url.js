// Test if Supabase URL is accessible
const testUrl = 'https://avquikcghthqcwiscldk.supabase.co';

console.log('Testing URL:', testUrl);

// Test with fetch
fetch(testUrl)
  .then(response => {
    console.log('✅ URL is accessible:', response.status);
  })
  .catch(error => {
    console.log('❌ URL is not accessible:', error.message);
  });
