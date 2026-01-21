const express = require('express');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// ⚠️ SECURITY ISSUE: Hardcoded secret key (Exercise 02)
const INTERNAL_API_KEY = 'sk-internal-1234567890abcdefghijklmnopqrstuv';

// ⚠️ SECURITY ISSUE: Logging sensitive data
console.log('Starting app with DB password:', process.env.DB_PASSWORD);

app.get('/', (req, res) => {
  res.json({
    message: 'Vulnerable Demo App',
    warning: 'This app contains intentional security issues for educational purposes'
  });
});

// ⚠️ SECURITY ISSUE: Exposing API keys in endpoint
app.get('/config', (req, res) => {
  res.json({
    stripe_key: process.env.STRIPE_SECRET_KEY,
    api_key: INTERNAL_API_KEY,
    db_host: process.env.DB_HOST
  });
});

// ⚠️ SECURITY ISSUE: Hardcoded AWS credentials
const awsConfig = {
  accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
  secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
  region: 'us-east-1'
};

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  // ⚠️ SECURITY ISSUE: Logging JWT secret
  console.log('JWT Secret:', process.env.JWT_SECRET);
});
