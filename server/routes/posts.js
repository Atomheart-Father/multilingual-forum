const express = require('express');
const router = express.Router();

// In-memory storage for demo (replace with database in production)
let posts = [
  {
    id: '1',
    title: 'Welcome to the Multilingual Forum!',
    content: 'This is a revolutionary platform where people from all over the world can communicate without language barriers. Post in your native language and read in your preferred language!',
    author: 'Admin',
    language: 'en',
    timestamp: new Date('2024-01-01T12:00:00Z').toISOString(),
    likes: 15,
    replies: []
  },
  {
    id: '2',
    title: 'Bonjour le monde!',
    content: 'Je suis très excité de pouvoir communiquer avec des gens du monde entier. Cette technologie va vraiment changer la façon dont nous interagissons en ligne.',
    author: 'Pierre',
    language: 'fr',
    timestamp: new Date('2024-01-02T10:30:00Z').toISOString(),
    likes: 8,
    replies: []
  },
  {
    id: '3',
    title: '¡Hola comunidad!',
    content: 'Estoy impresionado por esta plataforma. Finalmente podemos romper las barreras del idioma y conectar con personas de todo el mundo de manera más efectiva.',
    author: 'María',
    language: 'es',
    timestamp: new Date('2024-01-02T14:15:00Z').toISOString(),
    likes: 12,
    replies: []
  }
];

let nextId = 4;

// GET /api/posts - Get all posts
router.get('/', (req, res) => {
  const { page = 1, limit = 10, language } = req.query;
  
  let filteredPosts = posts;
  
  // Filter by language if specified
  if (language) {
    filteredPosts = posts.filter(post => post.language === language);
  }
  
  // Sort by timestamp (newest first)
  filteredPosts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  // Pagination
  const startIndex = (page - 1) * limit;
  const endIndex = startIndex + parseInt(limit);
  const paginatedPosts = filteredPosts.slice(startIndex, endIndex);
  
  res.json({
    posts: paginatedPosts,
    pagination: {
      currentPage: parseInt(page),
      totalPages: Math.ceil(filteredPosts.length / limit),
      totalPosts: filteredPosts.length,
      hasNext: endIndex < filteredPosts.length,
      hasPrev: startIndex > 0
    }
  });
});

// GET /api/posts/:id - Get specific post
router.get('/:id', (req, res) => {
  const post = posts.find(p => p.id === req.params.id);
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  res.json(post);
});

// POST /api/posts - Create new post
router.post('/', (req, res) => {
  const { title, content, author, language = 'en' } = req.body;
  
  if (!title || !content || !author) {
    return res.status(400).json({
      error: 'Missing required fields: title, content, author'
    });
  }
  
  if (title.length > 200) {
    return res.status(400).json({
      error: 'Title too long. Maximum 200 characters allowed.'
    });
  }
  
  if (content.length > 5000) {
    return res.status(400).json({
      error: 'Content too long. Maximum 5000 characters allowed.'
    });
  }
  
  const newPost = {
    id: String(nextId++),
    title: title.trim(),
    content: content.trim(),
    author: author.trim(),
    language,
    timestamp: new Date().toISOString(),
    likes: 0,
    replies: []
  };
  
  posts.unshift(newPost); // Add to beginning
  
  res.status(201).json(newPost);
});

// PUT /api/posts/:id/like - Like/unlike a post
router.put('/:id/like', (req, res) => {
  const post = posts.find(p => p.id === req.params.id);
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  const { action = 'like' } = req.body; // 'like' or 'unlike'
  
  if (action === 'like') {
    post.likes++;
  } else if (action === 'unlike' && post.likes > 0) {
    post.likes--;
  }
  
  res.json({ likes: post.likes });
});

// POST /api/posts/:id/reply - Add reply to post
router.post('/:id/reply', (req, res) => {
  const post = posts.find(p => p.id === req.params.id);
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  const { content, author, language = 'en' } = req.body;
  
  if (!content || !author) {
    return res.status(400).json({
      error: 'Missing required fields: content, author'
    });
  }
  
  if (content.length > 2000) {
    return res.status(400).json({
      error: 'Reply too long. Maximum 2000 characters allowed.'
    });
  }
  
  const reply = {
    id: String(Date.now()), // Simple ID generation for demo
    content: content.trim(),
    author: author.trim(),
    language,
    timestamp: new Date().toISOString(),
    likes: 0
  };
  
  post.replies.push(reply);
  
  res.status(201).json(reply);
});

// DELETE /api/posts/:id - Delete post (admin only for demo)
router.delete('/:id', (req, res) => {
  const postIndex = posts.findIndex(p => p.id === req.params.id);
  
  if (postIndex === -1) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  posts.splice(postIndex, 1);
  
  res.json({ message: 'Post deleted successfully' });
});

// GET /api/posts/stats/summary - Get forum statistics
router.get('/stats/summary', (req, res) => {
  const stats = {
    totalPosts: posts.length,
    totalReplies: posts.reduce((sum, post) => sum + post.replies.length, 0),
    totalLikes: posts.reduce((sum, post) => sum + post.likes, 0),
    languagesUsed: [...new Set(posts.map(post => post.language))].length,
    recentActivity: posts.slice(0, 5).map(post => ({
      id: post.id,
      title: post.title,
      author: post.author,
      timestamp: post.timestamp
    }))
  };
  
  res.json(stats);
});

module.exports = router; 