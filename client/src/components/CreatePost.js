import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeftIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';

function CreatePost({ user, userLanguage, supportedLanguages }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState(userLanguage);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      toast.error('Please login to create posts');
      return;
    }

    if (!title.trim() || !content.trim()) {
      toast.error('Please fill in both title and content');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title.trim(),
          content: content.trim(),
          author: user.username,
          language: selectedLanguage
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Post created successfully!');
        navigate(`/post/${data.id}`);
      } else {
        throw new Error(data.error || 'Failed to create post');
      }
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error(error.message || 'Failed to create post');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (title.trim() || content.trim()) {
      if (window.confirm('Are you sure you want to discard your post?')) {
        navigate('/');
      }
    } else {
      navigate('/');
    }
  };

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Login Required</h2>
          <p className="text-gray-600 mb-6">
            You need to be logged in to create posts. Please login to join the conversation!
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={handleCancel}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-2" />
          Back to Forum
        </button>
        
        <h1 className="text-3xl font-bold text-gray-900">Create New Post</h1>
        <p className="text-gray-600 mt-2">
          Share your thoughts with the global community. Write in any language - 
          our AI will help others understand you!
        </p>
      </div>

      {/* Form */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Language Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <GlobeAltIcon className="h-4 w-4 inline mr-1" />
              Post Language
            </label>
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              {Object.entries(supportedLanguages).map(([code, name]) => (
                <option key={code} value={code}>
                  {name}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Select the language you're writing in. Others will see your post translated to their preferred language.
            </p>
          </div>

          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Title *
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="What's your post about?"
              maxLength={200}
              disabled={loading}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Make it descriptive and engaging</span>
              <span>{title.length}/200</span>
            </div>
          </div>

          {/* Content */}
          <div>
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
              Content *
            </label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={8}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
              placeholder="Share your thoughts, experiences, questions, or ideas..."
              maxLength={5000}
              disabled={loading}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Express yourself freely in your language</span>
              <span>{content.length}/5000</span>
            </div>
          </div>

          {/* Guidelines */}
          <div className="bg-blue-50 rounded-md p-4">
            <h3 className="text-sm font-medium text-blue-900 mb-2">Community Guidelines</h3>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Be respectful and kind to others</li>
              <li>• Write in any language you're comfortable with</li>
              <li>• Share genuine thoughts and experiences</li>
              <li>• Avoid spam, hate speech, or harmful content</li>
            </ul>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={handleCancel}
              className="px-6 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50"
              disabled={loading || !title.trim() || !content.trim()}
            >
              {loading ? 'Creating...' : 'Create Post'}
            </button>
          </div>
        </form>
      </div>

      {/* Preview Note */}
      {(title.trim() || content.trim()) && (
        <div className="mt-4 p-4 bg-yellow-50 rounded-md">
          <p className="text-sm text-yellow-800">
            💡 <strong>Preview:</strong> Your post will appear in {supportedLanguages[selectedLanguage]} 
            to you, but others will see it automatically translated to their preferred language.
          </p>
        </div>
      )}
    </div>
  );
}

export default CreatePost; 