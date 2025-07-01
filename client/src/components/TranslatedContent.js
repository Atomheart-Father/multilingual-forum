import React, { useState, useEffect } from 'react';
import { ArrowPathIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

function TranslatedContent({ content, sourceLanguage, targetLanguage, className = '' }) {
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showOriginal, setShowOriginal] = useState(false);

  // 安全检查 props
  const safeContent = content || '';
  const safeSourceLang = sourceLanguage || 'auto';
  const safeTargetLang = targetLanguage || 'en';

  const translateContent = async () => {
    if (!safeContent.trim()) {
      setTranslatedText(safeContent);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/translate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: safeContent,
          source_lang: safeSourceLang,
          target_lang: safeTargetLang,
          service: 'local' // Use local translation by default
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setTranslatedText(data.translated_text || safeContent);
        setError(null);
      } else {
        console.error('Translation API error:', data);
        setError('翻译服务暂时不可用');
        setTranslatedText(safeContent); // Fallback to original
      }
    } catch (error) {
      console.error('Translation error:', error);
      setError('翻译失败，显示原文');
      setTranslatedText(safeContent); // Fallback to original content
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!safeContent.trim() || safeSourceLang === safeTargetLang) {
      setTranslatedText(safeContent);
      setLoading(false);
      setError(null);
      return;
    }

    // Add error boundary
    try {
      translateContent();
    } catch (error) {
      console.error('Translation component error:', error);
      setTranslatedText(safeContent);
      setError('组件错误');
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [content, sourceLanguage, targetLanguage]);

  const handleRetry = () => {
    try {
      translateContent();
    } catch (error) {
      console.error('Retry error:', error);
      setError('Retry failed');
    }
  };

  const toggleOriginal = () => {
    setShowOriginal(!showOriginal);
  };

  // If same language or no content, just show content directly
  if (!safeContent || safeSourceLang === safeTargetLang) {
    return <span className={className}>{safeContent}</span>;
  }

  const displayText = showOriginal ? safeContent : (translatedText || safeContent);

  return (
    <div className={`relative ${className}`}>
      <span className="block">
        {displayText}
      </span>

      {/* Translation Controls */}
      {safeSourceLang !== safeTargetLang && (
        <div className="flex items-center gap-2 mt-2 text-xs">
          {loading && (
            <div className="flex items-center text-blue-600">
              <ArrowPathIcon className="h-3 w-3 animate-spin mr-1" />
              <span>Translating...</span>
            </div>
          )}

          {error && (
            <div className="flex items-center text-red-600">
              <ExclamationTriangleIcon className="h-3 w-3 mr-1" />
              <span>{error}</span>
              <button
                onClick={handleRetry}
                className="ml-2 underline hover:no-underline"
              >
                Retry
              </button>
            </div>
          )}

          {!loading && !error && translatedText && translatedText !== safeContent && (
            <div className="flex items-center gap-2">
              <span className="text-green-600 text-xs">
                ✓ 已从 {safeSourceLang.toUpperCase()} 翻译到 {safeTargetLang.toUpperCase()}
              </span>
              <button
                onClick={toggleOriginal}
                className="text-blue-600 hover:text-blue-700 underline hover:no-underline text-xs"
              >
                {showOriginal ? '显示翻译' : '显示原文'}
              </button>
            </div>
          )}

          {!loading && !error && !translatedText && (
            <button
              onClick={handleRetry}
              className="text-blue-600 hover:text-blue-700 underline hover:no-underline"
            >
              Translate to {safeTargetLang.toUpperCase()}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default TranslatedContent; 