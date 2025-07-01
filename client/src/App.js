import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ForumHome from './components/ForumHome';
import PostDetail from './components/PostDetail';
import CreatePost from './components/CreatePost';
import Settings from './components/Settings';
import ErrorBoundary from './components/ErrorBoundary';
import { toast } from 'react-toastify';
import config from './config';

function App() {
  const [user, setUser] = useState(null);
  const [userLanguage, setUserLanguage] = useState('en');
  const [supportedLanguages, setSupportedLanguages] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load supported languages
    fetchSupportedLanguages();
    
    // Load user from localStorage or create demo user
    const savedUser = localStorage.getItem('forumUser');
    if (savedUser) {
      try {
        const parsedUser = JSON.parse(savedUser);
        setUser(parsedUser);
        setUserLanguage(parsedUser.preferredLanguage || 'en');
      } catch (error) {
        console.error('Error parsing saved user:', error);
        createDemoUser();
      }
    } else {
      createDemoUser();
    }
    
    setLoading(false);
  }, []);

  const fetchSupportedLanguages = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/translate/languages`);
      const languages = await response.json();
      setSupportedLanguages(languages);
    } catch (error) {
      console.error('Error fetching languages:', error);
      // Fallback languages
      setSupportedLanguages({
        'en': 'English',
        'zh': 'Chinese (Simplified)',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean'
      });
    }
  };

  const createDemoUser = () => {
    const demoUser = {
      id: '1',
      username: 'demo_user',
      email: 'demo@example.com',
      preferredLanguage: 'en'
    };
    setUser(demoUser);
    setUserLanguage('en');
    localStorage.setItem('forumUser', JSON.stringify(demoUser));
  };

  const updateUserLanguage = async (newLanguage) => {
    try {
      const updatedUser = { ...user, preferredLanguage: newLanguage };
      setUser(updatedUser);
      setUserLanguage(newLanguage);
      localStorage.setItem('forumUser', JSON.stringify(updatedUser));
      
      toast.success(`Language changed to ${supportedLanguages[newLanguage] || newLanguage}`);
    } catch (error) {
      console.error('Error updating language:', error);
      toast.error('Failed to update language preference');
    }
  };

  const loginUser = (userData) => {
    setUser(userData);
    setUserLanguage(userData.preferredLanguage || 'en');
    localStorage.setItem('forumUser', JSON.stringify(userData));
    toast.success(`Welcome, ${userData.username}!`);
  };

  const logoutUser = () => {
    setUser(null);
    setUserLanguage('en');
    localStorage.removeItem('forumUser');
    toast.info('Logged out successfully');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Multilingual Forum...</p>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        <Header 
          user={user}
          userLanguage={userLanguage}
          supportedLanguages={supportedLanguages}
          onLanguageChange={updateUserLanguage}
          onLogin={loginUser}
          onLogout={logoutUser}
        />
        
        <main className="container mx-auto px-4 py-8">
          <ErrorBoundary>
            <Routes>
              <Route 
                path="/" 
                element={
                  <ErrorBoundary>
                    <ForumHome 
                      user={user}
                      userLanguage={userLanguage}
                      supportedLanguages={supportedLanguages}
                    />
                  </ErrorBoundary>
                } 
              />
              <Route 
                path="/post/:id" 
                element={
                  <ErrorBoundary>
                    <PostDetail 
                      user={user}
                      userLanguage={userLanguage}
                      supportedLanguages={supportedLanguages}
                    />
                  </ErrorBoundary>
                } 
              />
              <Route 
                path="/create" 
                element={
                  <ErrorBoundary>
                    <CreatePost 
                      user={user}
                      userLanguage={userLanguage}
                      supportedLanguages={supportedLanguages}
                    />
                  </ErrorBoundary>
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <ErrorBoundary>
                    <Settings 
                      user={user}
                      userLanguage={userLanguage}
                      supportedLanguages={supportedLanguages}
                      onLanguageChange={updateUserLanguage}
                    />
                  </ErrorBoundary>
                } 
              />
            </Routes>
          </ErrorBoundary>
        </main>
        
        <footer className="bg-white border-t border-gray-200 mt-16">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center text-gray-600">
              <p>🌍 Multilingual Forum - Breaking Language Barriers</p>
              <p className="text-sm mt-2">
                Powered by AI Translation • Built with ❤️ for global communication
              </p>
            </div>
          </div>
        </footer>
      </div>
    </ErrorBoundary>
  );
}

export default App; 