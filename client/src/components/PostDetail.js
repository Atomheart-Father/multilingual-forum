import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeftIcon, 
  HeartIcon, 
  ChatBubbleLeftIcon, 
  ClockIcon,
  PaperAirplaneIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartIconSolid } from '@heroicons/react/24/solid';
import TranslatedContent from './TranslatedContent';
import { toast } from 'react-toastify';
import config from '../config';

function PostDetail({ user, userLanguage, supportedLanguages }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [replyLanguage, setReplyLanguage] = useState(userLanguage);
  const [submittingReply, setSubmittingReply] = useState(false);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchPost = React.useCallback(async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}${config.API_ENDPOINTS.POSTS}/${id}`);
      const data = await response.json();

      if (response.ok) {
        setPost(data);
      } else {
        throw new Error(data.error || 'Post not found');
      }
    } catch (error) {
      console.error('Error fetching post:', error);
      toast.error('Failed to load post');
      navigate('/');
    } finally {
      setLoading(false);
    }
  }, [id, navigate]);

  useEffect(() => {
    fetchPost();
  }, [fetchPost]);

  const handleLike = async () => {
    if (!user) {
      toast.info('Please login to like posts');
      return;
    }

    const action = liked ? 'unlike' : 'like';

    try {
      const response = await fetch(`${config.API_BASE_URL}${config.API_ENDPOINTS.POSTS}/${id}/like`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      });

      const data = await response.json();

      if (response.ok) {
        setPost(prev => ({ ...prev, likes: data.likes }));
        setLiked(!liked);
      } else {
        throw new Error(data.error || 'Failed to update like');
      }
    } catch (error) {
      console.error('Error updating like:', error);
      toast.error('Failed to update like');
    }
  };

  const handleReplySubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      toast.info('Please login to reply');
      return;
    }

    if (!replyContent.trim()) {
      toast.error('Please enter a reply');
      return;
    }

    setSubmittingReply(true);
    try {
      const response = await fetch(`${config.API_BASE_URL}${config.API_ENDPOINTS.POSTS}/${id}/reply`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: replyContent.trim(),
          author: user.username,
          language: replyLanguage
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setPost(prev => ({
          ...prev,
          replies: [...(prev.replies || []), data]
        }));
        setReplyContent('');
        toast.success('Reply posted successfully!');
      } else {
        throw new Error(data.error || 'Failed to post reply');
      }
    } catch (error) {
      console.error('Error posting reply:', error);
      toast.error(error.message || 'Failed to post reply');
    } finally {
      setSubmittingReply(false);
    }
  };

  const getLanguageBadgeClass = (language) => {
    const baseClass = 'language-badge';
    return `${baseClass} ${language || 'default'}`;
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

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading post...</p>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Post Not Found</h2>
        <p className="text-gray-600 mb-6">The post you're looking for doesn't exist or has been removed.</p>
        <button
          onClick={() => navigate('/')}
          className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
        >
          Back to Forum
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Navigation */}
      <button
        onClick={() => navigate('/')}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-6 transition-colors"
      >
        <ArrowLeftIcon className="h-4 w-4 mr-2" />
        Back to Forum
      </button>

      {/* Main Post */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        {/* Post Header */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="h-12 w-12 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-white text-lg font-medium">
                {post.author.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">{post.author}</h3>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <ClockIcon className="h-4 w-4" />
                <span>{formatTimestamp(post.timestamp)}</span>
                <span className={getLanguageBadgeClass(post.language)}>
                  {supportedLanguages[post.language] || post.language.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Post Content */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            <TranslatedContent
              content={post.title}
              sourceLanguage={post.language}
              targetLanguage={userLanguage}
            />
          </h1>
          <div className="text-gray-700 text-lg leading-relaxed">
            <TranslatedContent
              content={post.content}
              sourceLanguage={post.language}
              targetLanguage={userLanguage}
            />
          </div>
        </div>

        {/* Post Actions */}
        <div className="flex items-center space-x-6 pt-4 border-t border-gray-100">
          <button
            onClick={handleLike}
            className={`flex items-center space-x-2 transition-colors ${
              liked
                ? 'text-red-600 hover:text-red-700'
                : 'text-gray-500 hover:text-red-600'
            }`}
          >
            {liked ? (
              <HeartIconSolid className="h-6 w-6" />
            ) : (
              <HeartIcon className="h-6 w-6" />
            )}
            <span className="font-medium">{post.likes}</span>
            <span>Likes</span>
          </button>

          <div className="flex items-center space-x-2 text-gray-500">
            <ChatBubbleLeftIcon className="h-6 w-6" />
            <span className="font-medium">{post.replies?.length || 0}</span>
            <span>Replies</span>
          </div>
        </div>
      </div>

      {/* Reply Form */}
      {user ? (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Add a Reply</h3>
          <form onSubmit={handleReplySubmit} className="space-y-4">
            <div className="flex items-center space-x-4 mb-4">
              <div className="h-10 w-10 bg-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white font-medium">
                  {user.username.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-900">{user.username}</span>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500">Reply in:</span>
                  <select
                    value={replyLanguage}
                    onChange={(e) => setReplyLanguage(e.target.value)}
                    className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    {Object.entries(supportedLanguages).map(([code, name]) => (
                      <option key={code} value={code}>{name}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <textarea
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
              rows={4}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
              placeholder="Share your thoughts on this post..."
              maxLength={2000}
              disabled={submittingReply}
            />
            
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500">{replyContent.length}/2000</span>
              <button
                type="submit"
                className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50"
                disabled={submittingReply || !replyContent.trim()}
              >
                <PaperAirplaneIcon className="h-4 w-4" />
                <span>{submittingReply ? 'Posting...' : 'Post Reply'}</span>
              </button>
            </div>
          </form>
        </div>
      ) : (
        <div className="bg-gray-50 rounded-lg border border-gray-200 p-6 mb-6 text-center">
          <p className="text-gray-600">
            <button 
              onClick={() => toast.info('Please login to join the conversation')}
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              Login
            </button>
            {' '}to join the conversation and reply to this post.
          </p>
        </div>
      )}

      {/* Replies */}
      <div className="space-y-4">
        {(post.replies?.length || 0) > 0 ? (
          <>
            <h3 className="text-xl font-semibold text-gray-900">
              Replies ({post.replies?.length || 0})
            </h3>
            {(post.replies || []).map((reply) => (
              <div key={reply.id} className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-start space-x-3">
                  <div className="h-10 w-10 bg-gray-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {reply.author.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="font-medium text-gray-900">{reply.author}</span>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <ClockIcon className="h-3 w-3" />
                        <span>{formatTimestamp(reply.timestamp)}</span>
                        <span className={getLanguageBadgeClass(reply.language)}>
                          {supportedLanguages[reply.language] || reply.language.toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div className="text-gray-700">
                      <TranslatedContent
                        content={reply.content}
                        sourceLanguage={reply.language}
                        targetLanguage={userLanguage}
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <ChatBubbleLeftIcon className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No replies yet. Be the first to share your thoughts!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PostDetail; 