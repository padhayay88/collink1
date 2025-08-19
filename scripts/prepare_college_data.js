const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Ensure the processed data directory exists
const processedDir = path.join(__dirname, '../data/processed');
if (!fs.existsSync(processedDir)) {
  console.log('Creating processed data directory...');
  fs.mkdirSync(processedDir, { recursive: true });
}

// Run the Python script to process college data
console.log('Processing college data...');
try {
  execSync('python process_college_data.py', { stdio: 'inherit' });
  console.log('College data processing completed successfully!');
} catch (error) {
  console.error('Error processing college data:', error);
  process.exit(1);
}

// Copy the processed data to the public directory for the frontend
const publicDataDir = path.join(__dirname, '../frontend/public/data');
if (!fs.existsSync(publicDataDir)) {
  console.log('Creating public data directory...');
  fs.mkdirSync(publicDataDir, { recursive: true });
}

// Copy the processed files
const filesToCopy = [
  'colleges_by_rank.json',
  'colleges_by_state.json',
  'colleges_by_category.json'
];

filesToCopy.forEach(file => {
  const source = path.join(processedDir, file);
  const dest = path.join(publicDataDir, file);
  
  if (fs.existsSync(source)) {
    console.log(`Copying ${file} to public directory...`);
    fs.copyFileSync(source, dest);
  } else {
    console.warn(`Warning: ${file} not found in processed data`);
  }
});

// Also ensure the large comprehensive database is available to the frontend (for cache fallback)
(() => {
  const rootJson = path.join(__dirname, '../comprehensive_college_database.json');
  const publicRoot = path.join(__dirname, '../frontend/public');
  const target = path.join(publicRoot, 'comprehensive_college_database.json');
  try {
    if (fs.existsSync(rootJson)) {
      if (!fs.existsSync(publicRoot)) {
        fs.mkdirSync(publicRoot, { recursive: true });
      }
      console.log('Copying comprehensive_college_database.json to frontend/public ...');
      fs.copyFileSync(rootJson, target);
    } else {
      console.warn('Warning: comprehensive_college_database.json not found at repo root');
    }
  } catch (e) {
    console.warn('Warning: failed to copy comprehensive_college_database.json:', e.message);
  }
})();

console.log('Data preparation completed!');

