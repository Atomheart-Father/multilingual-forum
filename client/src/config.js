// 🌍 多语言AI论坛 - 前端配置

// 根据环境选择API URL
const getApiUrl = () => {
  // 1. 优先使用环境变量
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // 2. 生产环境使用Render后端
  if (process.env.NODE_ENV === 'production') {
    return 'https://multilingual-forum-api.onrender.com';
  }
  
  // 3. 开发环境使用本地后端
  return 'http://localhost:3001';
};

const config = {
  // API基础地址 - 根据环境自动选择
  API_BASE_URL: getApiUrl(),
  
  // 环境判断
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  
  // 应用配置
  APP_NAME: '多语言AI论坛',
  APP_VERSION: '1.0.0',
  
  // 默认设置
  DEFAULT_LANGUAGE: 'zh',
  SUPPORTED_LANGUAGES: [
    'zh', 'en', 'ja', 'ko', 'es', 'fr', 'de', 'it', 'pt', 'ru',
    'ar', 'hi', 'nl', 'sv', 'da', 'no', 'fi', 'pl', 'cs', 'hu',
    'tr', 'el', 'he', 'th', 'vi', 'id', 'ms', 'tl', 'uk', 'bg',
    'hr', 'sr', 'sl', 'sk', 'ro', 'et', 'lv', 'lt'
  ],
  
  // API端点
  API_ENDPOINTS: {
    POSTS: '/api/posts',
    TRANSLATE: '/api/translate',
    AUTH: '/api/auth',
    HEALTH: '/api/health'
  },
  
  // 调试模式
  DEBUG: process.env.REACT_APP_DEBUG === 'true',
  
  // 翻译服务配置
  TRANSLATION: {
    DEFAULT_SERVICE: 'local',
    SERVICES: ['local', 'openai', 'azure', 'google', 'deepl']
  }
};

// 开发环境日志
if (config.isDevelopment || config.DEBUG) {
  console.log('🔧 论坛配置:', {
    API_URL: config.API_BASE_URL,
    Environment: process.env.NODE_ENV,
    Debug: config.DEBUG
  });
}

export default config; 