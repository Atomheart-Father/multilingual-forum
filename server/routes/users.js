const express = require('express');
const router = express.Router();

// GET /api/users - Get all users (for demo)
router.get('/', (req, res) => {
  const users = [
    { id: '1', username: 'admin', preferredLanguage: 'en', joinDate: '2024-01-01' },
    { id: '2', username: 'pierre', preferredLanguage: 'fr', joinDate: '2024-01-02' },
    { id: '3', username: 'maria', preferredLanguage: 'es', joinDate: '2024-01-02' }
  ];
  
  res.json(users);
});

// GET /api/users/:id - Get specific user
router.get('/:id', (req, res) => {
  const users = [
    { id: '1', username: 'admin', preferredLanguage: 'en', joinDate: '2024-01-01' },
    { id: '2', username: 'pierre', preferredLanguage: 'fr', joinDate: '2024-01-02' },
    { id: '3', username: 'maria', preferredLanguage: 'es', joinDate: '2024-01-02' }
  ];
  
  const user = users.find(u => u.id === req.params.id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json(user);
});

module.exports = router; 