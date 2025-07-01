import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  GlobeAltIcon, 
  PlusIcon, 
  Cog6ToothIcon,
  UserIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';
import LoginModal from './LoginModal';

function Header({ user, userLanguage, supportedLanguages, onLanguageChange, onLogin, onLogout }) {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <GlobeAltIcon className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Multilingual Forum</h1>
                <p className="text-xs text-gray-500 -mt-1">Breaking Language Barriers</p>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-6">
              <Link 
                to="/" 
                className={`font-medium transition-colors ${
                  isActive('/') 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Home
              </Link>
              <Link 
                to="/create" 
                className={`flex items-center space-x-1 font-medium transition-colors ${
                  isActive('/create') 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <PlusIcon className="h-4 w-4" />
                <span>Create Post</span>
              </Link>
            </nav>

            {/* User Actions */}
            <div className="flex items-center space-x-4">
              {/* Language Selector */}
              <div className="relative">
                <button
                  onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
                  className="flex items-center space-x-1 px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                >
                  <GlobeAltIcon className="h-4 w-4" />
                  <span className="text-sm font-medium">
                    {supportedLanguages[userLanguage] || userLanguage.toUpperCase()}
                  </span>
                </button>
                
                {showLanguageDropdown && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                    <div className="py-1 max-h-64 overflow-y-auto">
                      {Object.entries(supportedLanguages).map(([code, name]) => (
                        <button
                          key={code}
                          onClick={() => {
                            onLanguageChange(code);
                            setShowLanguageDropdown(false);
                          }}
                          className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 transition-colors ${
                            userLanguage === code 
                              ? 'bg-primary-50 text-primary-700 font-medium' 
                              : 'text-gray-700'
                          }`}
                        >
                          {name}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* User Menu */}
              {user ? (
                <div className="relative">
                  <button
                    onClick={() => setShowUserDropdown(!showUserDropdown)}
                    className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-100 transition-colors"
                  >
                    <div className="h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">
                        {user.username.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="text-sm font-medium text-gray-700 hidden md:block">
                      {user.username}
                    </span>
                  </button>

                  {showUserDropdown && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                      <div className="py-1">
                        <div className="px-4 py-2 border-b border-gray-100">
                          <p className="text-sm font-medium text-gray-900">{user.username}</p>
                          <p className="text-xs text-gray-500">{user.email}</p>
                        </div>
                        <Link
                          to="/settings"
                          className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                          onClick={() => setShowUserDropdown(false)}
                        >
                          <Cog6ToothIcon className="h-4 w-4" />
                          <span>Settings</span>
                        </Link>
                        <button
                          onClick={() => {
                            onLogout();
                            setShowUserDropdown(false);
                          }}
                          className="flex items-center space-x-2 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                        >
                          <ArrowRightOnRectangleIcon className="h-4 w-4" />
                          <span>Logout</span>
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  <UserIcon className="h-4 w-4" />
                  <span>Login</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-gray-200 bg-gray-50">
          <div className="container mx-auto px-4 py-2">
            <div className="flex justify-center space-x-8">
              <Link 
                to="/" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/') 
                    ? 'text-primary-600' 
                    : 'text-gray-600'
                }`}
              >
                Home
              </Link>
              <Link 
                to="/create" 
                className={`text-sm font-medium transition-colors ${
                  isActive('/create') 
                    ? 'text-primary-600' 
                    : 'text-gray-600'
                }`}
              >
                Create Post
              </Link>
            </div>
          </div>
        </div>
      </header>

      {showLoginModal && (
        <LoginModal
          onClose={() => setShowLoginModal(false)}
          onLogin={onLogin}
        />
      )}
    </>
  );
}

export default Header; 