import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  HeartIcon, 
  ChatBubbleLeftIcon, 
  ClockIcon,
  PlusIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartIconSolid } from '@heroicons/react/24/solid';
import TranslatedContent from './TranslatedContent';
import { toast } from 'react-toastify';
import config from '../config';

function ForumHome({ user, userLanguage, supportedLanguages }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [likedPosts, setLikedPosts] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchPosts = React.useCallback(async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}${config.API_ENDPOINTS.POSTS}/`);
      const data = await response.json();
      
      if (response.ok) {
        setPosts(data.posts);
      } else {
        throw new Error(data.error || 'Failed to fetch posts');
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
      toast.error('Failed to load posts');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const handleLike = async (postId) => {
    if (!user) {
      toast.info('Please login to like posts');
      return;
    }

    const isLiked = likedPosts.has(postId);
    const action = isLiked ? 'unlike' : 'like';

    try {
      const response = await fetch(`${config.API_BASE_URL}${config.API_ENDPOINTS.POSTS}/${postId}/like`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      });

      const data = await response.json();
      
      if (response.ok) {
        // Update posts with new like count
        setPosts(posts.map(post => 
          post.id === postId 
            ? { ...post, likes: data.likes }
            : post
        ));

        // Update liked posts set
        const newLikedPosts = new Set(likedPosts);
        if (isLiked) {
          newLikedPosts.delete(postId);
        } else {
          newLikedPosts.add(postId);
        }
        setLikedPosts(newLikedPosts);
      } else {
        throw new Error(data.error || 'Failed to update like');
      }
    } catch (error) {
      console.error('Error updating like:', error);
      toast.error('Failed to update like');
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor(diffMs / (1000 * 60));

    if (diffDays > 0) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else if (diffHours > 0) {
      return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffMinutes > 0) {
      return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
    } else {
      return 'Just now';
    }
  };

  const filteredPosts = posts.filter(post => {
    if (!searchTerm) return true;
    const searchLower = searchTerm.toLowerCase();
    return (
      post.title.toLowerCase().includes(searchLower) ||
      post.content.toLowerCase().includes(searchLower) ||
      post.author.toLowerCase().includes(searchLower)
    );
  });

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading posts...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🌍 Welcome to the Multilingual Forum
        </h1>
        <p className="text-gray-600 mb-6">
          Share your thoughts in any language. All posts are automatically translated to your preferred language: {' '}
          <span className="font-semibold text-primary-600">
            {supportedLanguages[userLanguage] || userLanguage}
          </span>
        </p>

        {/* Action Bar */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          {/* Search */}
          <div className="relative flex-1 md:w-64">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search posts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          <Link
            to="/create"
            className="flex items-center justify-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            <PlusIcon className="h-4 w-4" />
            <span>Create Post</span>
          </Link>
        </div>
      </div>

      {/* Posts List */}
      {filteredPosts.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
          <div className="text-gray-400 mb-4">
            <ChatBubbleLeftIcon className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No posts found</h3>
          <p className="text-gray-600 mb-6">
            {searchTerm 
              ? 'Try adjusting your search criteria.'
              : 'Be the first to start a conversation!'
            }
          </p>
          {!searchTerm && (
            <Link
              to="/create"
              className="inline-flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="h-4 w-4" />
              <span>Create First Post</span>
            </Link>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          {filteredPosts.map((post) => (
            <div key={post.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
              {/* Post Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {post.author.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{post.author}</h3>
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <ClockIcon className="h-4 w-4" />
                      <span>{formatTimestamp(post.timestamp)}</span>
                      {post.language !== userLanguage && (
                        <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full">
                          源语言：{supportedLanguages[post.language] || post.language.toUpperCase()}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Post Content */}
              <Link to={`/post/${post.id}`} className="block group">
                <h2 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors">
                  <TranslatedContent
                    content={post.title}
                    sourceLanguage={post.language}
                    targetLanguage={userLanguage}
                  />
                </h2>
                <div className="text-gray-700 line-clamp-3">
                  <TranslatedContent
                    content={post.content}
                    sourceLanguage={post.language}
                    targetLanguage={userLanguage}
                  />
                </div>
              </Link>

              {/* Post Actions */}
              <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => handleLike(post.id)}
                    className={`flex items-center space-x-1 transition-colors ${
                      likedPosts.has(post.id)
                        ? 'text-red-600 hover:text-red-700'
                        : 'text-gray-500 hover:text-red-600'
                    }`}
                  >
                    {likedPosts.has(post.id) ? (
                      <HeartIconSolid className="h-5 w-5" />
                    ) : (
                      <HeartIcon className="h-5 w-5" />
                    )}
                    <span className="text-sm font-medium">{post.likes}</span>
                  </button>

                  <Link
                    to={`/post/${post.id}`}
                    className="flex items-center space-x-1 text-gray-500 hover:text-primary-600 transition-colors"
                  >
                    <ChatBubbleLeftIcon className="h-5 w-5" />
                    <span className="text-sm font-medium">{post.replies.length}</span>
                  </Link>
                </div>

                <Link
                  to={`/post/${post.id}`}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors"
                >
                  Read more →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ForumHome; 