const express = require('express');
const router = express.Router();

// Simple in-memory user storage for demo
const users = [
  { id: '1', username: 'admin', email: 'admin@example.com', preferredLanguage: 'en' },
  { id: '2', username: 'pierre', email: 'pierre@example.com', preferredLanguage: 'fr' },
  { id: '3', username: 'maria', email: 'maria@example.com', preferredLanguage: 'es' }
];

// POST /api/auth/login - Simple login (no actual auth for demo)
router.post('/login', (req, res) => {
  const { username } = req.body;
  
  if (!username) {
    return res.status(400).json({ error: 'Username is required' });
  }
  
  let user = users.find(u => u.username.toLowerCase() === username.toLowerCase());
  
  if (!user) {
    // Create new user for demo
    user = {
      id: String(Date.now()),
      username: username.trim(),
      email: `${username.trim().toLowerCase()}@example.com`,
      preferredLanguage: 'en'
    };
    users.push(user);
  }
  
  res.json({
    user,
    token: 'demo-jwt-token' // In real app, generate actual JWT
  });
});

// GET /api/auth/me - Get current user
router.get('/me', (req, res) => {
  // In real app, verify JWT token
  const userId = req.headers['x-user-id'] || '1';
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(401).json({ error: 'User not found' });
  }
  
  res.json(user);
});

// PUT /api/auth/preferences - Update user preferences
router.put('/preferences', (req, res) => {
  const userId = req.headers['x-user-id'] || '1';
  const { preferredLanguage } = req.body;
  
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(401).json({ error: 'User not found' });
  }
  
  if (preferredLanguage) {
    user.preferredLanguage = preferredLanguage;
  }
  
  res.json(user);
});

module.exports = router; 