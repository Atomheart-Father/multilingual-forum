# 🌍 多语言AI论坛 | Multilingual AI Forum

[![GitHub](https://img.shields.io/github/license/your-username/multilingual-forum)](https://github.com/your-username/multilingual-forum)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

一个突破语言障碍的AI驱动多语言论坛平台，让全球用户能够用自己的母语自由交流。

[🚀 在线演示](https://your-demo-link.com) | [📖 文档](./docs/) | [🐛 问题反馈](https://github.com/your-username/multilingual-forum/issues)

## ✨ 核心特性

### 🔤 强大的多语言支持
- **30+种语言**：涵盖欧洲、亚洲、美洲主要语言
- **智能检测**：自动识别用户输入语言
- **实时翻译**：帖子和回复自动翻译到用户偏好语言
- **语言过滤**：按原始语言筛选内容

### 🤖 多引擎AI翻译
- **本地模型**：支持Hugging Face Transformers、Ollama等本地部署
- **云端API**：集成OpenAI、Google Translate、Azure Translator、DeepL
- **智能降级**：主服务失败时自动切换备用翻译服务
- **隐私保护**：本地翻译模式数据不离开服务器

### 🎨 现代化体验
- **响应式设计**：完美适配桌面和移动设备
- **Tailwind CSS**：美观现代的Material Design界面
- **实时交互**：即时翻译和动态内容加载
- **错误边界**：优雅的错误处理和用户反馈

### 🛠️ 技术架构
- **后端**：Python FastAPI + Uvicorn + Pydantic
- **前端**：React 18 + Tailwind CSS + React Router
- **翻译**：本地Transformers + 多云端API集成
- **部署**：Docker + Docker Compose + Vercel + Render

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8+ (推荐3.9+)
- **Node.js**: 16+ 
- **npm**: 7+
- **Git**: 最新版本

### ⚡ 一键启动

```bash
# 克隆仓库
git clone https://github.com/your-username/multilingual-forum.git
cd multilingual-forum

# 一键启动所有服务
./start.sh
```

这将自动：
1. 创建Python虚拟环境
2. 安装所有依赖
3. 启动后端API服务器 (http://localhost:3001)
4. 启动前端开发服务器 (http://localhost:3000)

### 🐳 Docker部署

```bash
# 使用Docker Compose启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 📖 详细配置

### 1. Python后端设置

```bash
cd server

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动FastAPI服务器
python main.py
```

后端服务器启动在 http://localhost:3001
- API文档: http://localhost:3001/docs
- 健康检查: http://localhost:3001/api/health

### 2. React前端设置

```bash
cd client

# 安装依赖
npm install

# 启动开发服务器
npm start
```

前端应用启动在 http://localhost:3000

### 3. 环境变量配置

复制环境变量模板：

```bash
cd server
cp env.example .env
```

编辑 `server/.env` 文件：

```env
# === 翻译服务API密钥 (可选) ===
OPENAI_API_KEY=your_openai_key
GOOGLE_TRANSLATE_KEY=your_google_key
AZURE_TRANSLATE_KEY=your_azure_key
AZURE_TRANSLATE_REGION=eastus
DEEPL_API_KEY=your_deepl_key

# === 本地模型配置 ===
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh
OLLAMA_SERVER_URL=http://localhost:11434

# === 服务器配置 ===
PORT=3001
NODE_ENV=development
ALLOWED_ORIGINS=http://localhost:3000

# === 速率限制 ===
RATE_LIMIT_MAX_REQUESTS=1000
RATE_LIMIT_WINDOW_MS=60000
```

## 🌐 免费部署方案

### 🆓 方案1: Vercel + Render (完全免费)

#### 前端部署到Vercel
1. Fork此仓库到你的GitHub
2. 在[Vercel](https://vercel.com)创建新项目
3. 配置构建设置：
   - **Framework**: Create React App
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Environment Variables**: 
     ```
     REACT_APP_API_URL=https://your-api.onrender.com
     ```

#### 后端部署到Render
1. 在[Render](https://render.com)创建Web Service
2. 连接GitHub仓库
3. 配置服务：
   - **Build Command**: `cd server && pip install -r requirements.txt`
   - **Start Command**: `cd server && python main.py`
   - **Environment Variables**: 添加必要的API密钥

### 🆓 方案2: 超简模式

使用 `server/main-ultra-simple.py` 进行最小依赖部署：

```bash
# 零外部依赖版本，使用Python标准库
python server/main-ultra-simple.py
```

特点：
- 100%使用Python标准库
- 内存数据存储
- 适合演示和快速测试

## 🔧 支持的翻译服务

### 本地模型 (推荐)
```env
# Hugging Face Transformers
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh

# Ollama LLM
LOCAL_MODEL_TYPE=ollama
OLLAMA_SERVER_URL=http://localhost:11434
```

### 云端API服务
- **OpenAI GPT**: 高质量AI翻译，上下文理解
- **DeepL**: 欧洲语言最佳，德语、法语、荷兰语优秀
- **Azure Translator**: 企业级稳定性
- **Google Translate**: 语言覆盖最广

## 🗣️ 支持的语言

<details>
<summary>点击查看所有支持的语言（30+种）</summary>

**欧洲语言**
- 🇬🇧 English
- 🇩🇪 German (德语)
- 🇫🇷 French (法语)
- 🇪🇸 Spanish (西班牙语)
- 🇮🇹 Italian (意大利语)
- 🇳🇱 Dutch (荷兰语)
- 🇵🇹 Portuguese (葡萄牙语)
- 🇷🇺 Russian (俄语)
- 🇵🇱 Polish (波兰语)
- 🇸🇪 Swedish (瑞典语)
- 🇩🇰 Danish (丹麦语)
- 🇳🇴 Norwegian (挪威语)
- 🇫🇮 Finnish (芬兰语)

**亚洲语言**
- 🇨🇳 Chinese (中文简体)
- 🇹🇼 Chinese Traditional (中文繁体)
- 🇯🇵 Japanese (日语)
- 🇰🇷 Korean (韩语)
- 🇮🇳 Hindi (印地语)
- 🇹🇭 Thai (泰语)
- 🇻🇳 Vietnamese (越南语)
- 🇮🇩 Indonesian (印尼语)

**其他语言**
- 🇸🇦 Arabic (阿拉伯语)
- 🇹🇷 Turkish (土耳其语)
- 🇮🇱 Hebrew (希伯来语)
- 🇬🇷 Greek (希腊语)

</details>

## 📊 项目架构

### 后端结构 (Python FastAPI)
```
server/
├── main.py              # FastAPI应用入口
├── models.py            # Pydantic数据模型
├── routes/              # API路由模块
│   ├── auth.py         # 用户认证
│   ├── posts.py        # 帖子管理
│   ├── translate.py    # 翻译服务
│   └── users.py        # 用户管理
├── middleware/          # 中间件
│   └── rate_limit.py   # 速率限制
├── main-ultra-simple.py # 零依赖版本
└── requirements.txt     # Python依赖
```

### 前端结构 (React)
```
client/
├── src/
│   ├── App.js          # 主应用组件
│   ├── components/     # React组件
│   │   ├── Header.js
│   │   ├── ForumHome.js
│   │   ├── PostDetail.js
│   │   ├── CreatePost.js
│   │   └── TranslatedContent.js
│   └── config.js       # 配置文件
└── package.json        # Node.js依赖
```

## 🔍 API文档

启动服务器后访问自动生成的API文档：
- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc

### 主要API端点

```bash
# 健康检查
GET /api/health

# 翻译服务
POST /api/translate/
GET /api/translate/languages

# 帖子管理
GET /api/posts/
POST /api/posts/
GET /api/posts/{id}
PUT /api/posts/{id}/like
POST /api/posts/{id}/reply

# 用户认证
POST /api/auth/login
POST /api/auth/register

# 用户管理
GET /api/users/me
PUT /api/users/preferences
```

## 🛡️ 安全特性

- **速率限制**: 防止API滥用
- **CORS配置**: 安全的跨域请求
- **输入验证**: Pydantic模型验证
- **错误处理**: 统一异常处理
- **本地翻译**: 数据隐私保护

## 🧪 测试

### 后端测试
```bash
cd server
python -m pytest test_server.py -v
```

### 本地翻译测试
```bash
cd server
python test_local_translation.py
```

### 部署测试
```bash
python test_deployment.py
```

## 📈 性能优化

- **异步处理**: 所有API使用async/await
- **翻译缓存**: 减少重复翻译请求
- **连接池**: 高效的HTTP客户端
- **懒加载**: 前端组件按需加载
- **CDN就绪**: 静态文件优化

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 支持

- 📖 [文档](./docs/)
- 🐛 [问题反馈](https://github.com/your-username/multilingual-forum/issues)
- 💬 [讨论](https://github.com/your-username/multilingual-forum/discussions)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [React](https://reactjs.org/) - 用户界面构建
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [Hugging Face](https://huggingface.co/) - 开源AI模型
- [OpenAI](https://openai.com/) - GPT翻译服务

---

<p align="center">
  <strong>🌍 让语言不再是沟通的障碍 | Breaking Language Barriers</strong>
</p> 