import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowLeftIcon, 
  GlobeAltIcon, 
  UserIcon,
  Cog6ToothIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { toast } from 'react-toastify';

function Settings({ user, userLanguage, supportedLanguages, onLanguageChange }) {
  const navigate = useNavigate();
  const [selectedLanguage, setSelectedLanguage] = useState(userLanguage);
  const [saving, setSaving] = useState(false);

  const handleSaveLanguage = async () => {
    if (selectedLanguage === userLanguage) {
      toast.info('Language preference unchanged');
      return;
    }

    setSaving(true);
    try {
      await onLanguageChange(selectedLanguage);
      toast.success('Language preference updated successfully!');
    } catch (error) {
      console.error('Error updating language:', error);
      toast.error('Failed to update language preference');
    } finally {
      setSaving(false);
    }
  };

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Login Required</h2>
          <p className="text-gray-600 mb-6">
            You need to be logged in to access settings.
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
          onClick={() => navigate('/')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-2" />
          Back to Forum
        </button>
        
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">
          Customize your forum experience
        </p>
      </div>

      <div className="space-y-6">
        {/* User Profile */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <UserIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-xl font-semibold text-gray-900">Profile</h2>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-white text-2xl font-medium">
                {user.username.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">{user.username}</h3>
              <p className="text-gray-600">{user.email}</p>
              <p className="text-sm text-gray-500">
                Current language: {supportedLanguages[userLanguage] || userLanguage}
              </p>
            </div>
          </div>
        </div>

        {/* Language Preferences */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <GlobeAltIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-xl font-semibold text-gray-900">Language Preferences</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label htmlFor="language-select" className="block text-sm font-medium text-gray-700 mb-2">
                Preferred Reading Language
              </label>
              <select
                id="language-select"
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
              <p className="text-sm text-gray-500 mt-1">
                All posts and replies will be automatically translated to this language for you.
              </p>
            </div>

            {selectedLanguage !== userLanguage && (
              <div className="bg-blue-50 rounded-md p-4">
                <div className="flex items-start space-x-2">
                  <InformationCircleIcon className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-blue-700">
                    <p className="font-medium mb-1">Language Change Preview</p>
                    <p>
                      You're changing from <strong>{supportedLanguages[userLanguage]}</strong> to{' '}
                      <strong>{supportedLanguages[selectedLanguage]}</strong>. 
                      This will affect how you see all content in the forum.
                    </p>
                  </div>
                </div>
              </div>
            )}

            <button
              onClick={handleSaveLanguage}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50"
              disabled={saving || selectedLanguage === userLanguage}
            >
              {saving ? 'Saving...' : 'Save Language Preference'}
            </button>
          </div>
        </div>

        {/* Translation Settings */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Cog6ToothIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-xl font-semibold text-gray-900">Translation Settings</h2>
          </div>

          <div className="space-y-4">
            <div className="bg-gray-50 rounded-md p-4">
              <h3 className="font-medium text-gray-900 mb-2">AI Translation Services</h3>
              <div className="text-sm text-gray-600 space-y-2">
                <p>• <strong>Primary:</strong> OpenAI GPT-3.5/4 (High quality, context-aware)</p>
                <p>• <strong>Fallback:</strong> Azure Translator, Google Translate, DeepL</p>
                <p>• <strong>Languages:</strong> 30+ supported languages</p>
              </div>
            </div>

            <div className="bg-green-50 rounded-md p-4">
              <h3 className="font-medium text-green-900 mb-2">Translation Quality</h3>
              <p className="text-sm text-green-700">
                Our AI maintains context, tone, and cultural nuances while translating. 
                You can always view the original text by clicking "Show original" on any translated content.
              </p>
            </div>
          </div>
        </div>

        {/* Forum Statistics */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Activity</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-md">
              <div className="text-2xl font-bold text-primary-600">0</div>
              <div className="text-sm text-gray-600">Posts Created</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-md">
              <div className="text-2xl font-bold text-primary-600">0</div>
              <div className="text-sm text-gray-600">Replies Posted</div>
            </div>
          </div>
        </div>

        {/* About */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">About Multilingual Forum</h2>
          
          <div className="text-sm text-gray-600 space-y-3">
            <p>
              <strong>Version:</strong> 1.0.0
            </p>
            <p>
              <strong>Mission:</strong> Breaking language barriers to connect people worldwide through AI-powered translation.
            </p>
            <p>
              <strong>Technology:</strong> Built with React, Node.js, and advanced AI translation services.
            </p>
            <p>
              <strong>Privacy:</strong> Your conversations are translated in real-time. We don't store personal translation data.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings; 