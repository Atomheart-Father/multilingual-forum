# 🌍 多语言AI论坛 | Multilingual AI Forum

[![GitHub](https://img.shields.io/github/license/your-username/multilingual-forum)](https://github.com/your-username/multilingual-forum)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

一个突破语言障碍的AI驱动多语言论坛平台，让全球用户能够用自己的母语自由交流。

[🚀 在线演示](https://your-demo-link.com) | [📖 文档](./docs/) | [🐛 问题反馈](https://github.com/your-username/multilingual-forum/issues)

## ✨ 特性

### 🔤 多语言支持
- **36+种语言**：支持中文、英语、日语、韩语、法语、德语、西班牙语等
- **智能检测**：自动检测用户输入语言
- **实时翻译**：帖子和回复自动翻译到用户偏好语言

### 🤖 AI翻译引擎
- **本地模型**：支持Hugging Face Transformers本地翻译
- **云端API**：集成OpenAI、Google Translate、Azure Translator、DeepL
- **智能降级**：服务失败时自动切换备用翻译服务
- **隐私保护**：本地翻译模式数据不离开服务器

### 🎨 现代化界面
- **响应式设计**：完美适配桌面和移动设备
- **Tailwind CSS**：美观现代的用户界面
- **暗黑模式**：即将支持
- **无障碍访问**：符合WCAG标准

### 🛠️ 技术栈
- **前端**：React 18 + Tailwind CSS + React Router
- **后端**：Python FastAPI + Uvicorn
- **翻译**：本地Transformers + 多云端API
- **部署**：Docker + Docker Compose

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 7+
- **Git**: 最新版本

### ⚡ 一键启动

```bash
# 克隆仓库
git clone https://github.com/your-username/multilingual-forum.git
cd multilingual-forum

# 设置后端环境（仅首次）
cd server
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# 一键启动所有服务
./start.sh
```

启动后访问：
- **论坛首页**: http://localhost:3000
- **API文档**: http://localhost:3001/docs

### 🐳 Docker部署

```bash
# 使用Docker Compose启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 📖 详细安装指南

### 1. 后端设置

```bash
cd server

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务器
python main.py
```

### 2. 前端设置

```bash
cd client

# 安装依赖
npm install

# 启动开发服务器
npm start
```

### 3. 环境变量配置

创建 `server/.env` 文件：

```env
# 翻译服务API密钥（可选）
OPENAI_API_KEY=your_openai_key
GOOGLE_TRANSLATE_KEY=your_google_key
AZURE_TRANSLATE_KEY=your_azure_key
DEEPL_API_KEY=your_deepl_key

# 本地模型配置
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh

# 服务器配置
PORT=3001
ALLOWED_ORIGINS=http://localhost:3000

# 速率限制
RATE_LIMIT_MAX_REQUESTS=1000
RATE_LIMIT_WINDOW_MS=60000
```

## 🌐 部署指南

### GitHub Pages + 云端后端

由于项目包含后端，推荐以下部署方案：

#### 前端部署到Vercel
1. Fork此仓库到你的GitHub
2. 在[Vercel](https://vercel.com)创建新项目
3. 选择你的GitHub仓库
4. 设置构建配置：
   - **Framework Preset**: Create React App
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

#### 后端部署到Railway/Render
1. 在[Railway](https://railway.app)或[Render](https://render.com)创建新服务
2. 连接你的GitHub仓库
3. 设置环境变量
4. 服务会自动部署

### Docker部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 扩展服务
docker-compose up --scale api=3
```

## 🔧 配置选项

### 翻译服务配置

项目支持多种翻译服务，可在 `server/.env` 中配置：

```env
# 本地模型（推荐，免费且隐私）
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh

# 或使用Ollama本地大模型
LOCAL_MODEL_TYPE=ollama
OLLAMA_SERVER_URL=http://localhost:11434

# 云端API（需要API密钥）
OPENAI_API_KEY=your_key
GOOGLE_TRANSLATE_KEY=your_key
AZURE_TRANSLATE_KEY=your_key
DEEPL_API_KEY=your_key
```

### 支持的语言

<details>
<summary>点击查看所有支持的语言（36种）</summary>

- 🇨🇳 中文 (简体/繁体)
- 🇺🇸 English
- 🇯🇵 日本語
- 🇰🇷 한국어  
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇮🇹 Italiano
- 🇵🇹 Português
- 🇷🇺 Русский
- 🇸🇦 العربية
- 🇮🇳 हिन्दी
- 🇳🇱 Nederlands
- 🇸🇪 Svenska
- 🇩🇰 Dansk
- 🇳🇴 Norsk
- 🇫🇮 Suomi
- 🇵🇱 Polski
- 🇨🇿 Čeština
- 🇭🇺 Magyar
- 🇹🇷 Türkçe
- 🇬🇷 Ελληνικά
- 🇮🇱 עברית
- 🇹🇭 ไทย
- 🇻🇳 Tiếng Việt
- 🇮🇩 Bahasa Indonesia
- 🇲🇾 Bahasa Melayu
- 🇵🇭 Filipino
- 🇺🇦 Українська
- 🇧🇬 Български
- 🇭🇷 Hrvatski
- 🇷🇸 Српски
- 🇸🇮 Slovenščina
- 🇸🇰 Slovenčina
- 🇷🇴 Română
- 🇪🇪 Eesti

</details>

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork**此仓库
2. **创建**特性分支：`git checkout -b feature/amazing-feature`
3. **提交**更改：`git commit -m 'Add amazing feature'`
4. **推送**到分支：`git push origin feature/amazing-feature`
5. **创建** Pull Request

### 开发指南

```bash
# 安装开发依赖
cd client && npm install
cd ../server && pip install -r requirements.txt

# 运行测试
npm test                    # 前端测试
python -m pytest          # 后端测试

# 代码格式化
npm run format             # 前端格式化
black server/             # 后端格式化
```

## 📝 API文档

启动服务器后，访问 http://localhost:3001/docs 查看完整的API文档。

### 主要API端点

- `GET /api/posts/` - 获取帖子列表
- `POST /api/posts/` - 创建新帖子
- `GET /api/posts/{id}/` - 获取特定帖子
- `POST /api/translate/` - 翻译文本
- `GET /api/translate/languages` - 获取支持的语言列表

## 🔒 安全性

- ✅ 速率限制防止滥用
- ✅ 输入验证和清理
- ✅ CORS配置
- ✅ 环境变量保护敏感信息
- ✅ 本地翻译模式保护隐私

## 🐛 故障排除

### 常见问题

<details>
<summary>启动时端口被占用</summary>

```bash
# 查找占用端口的进程
lsof -ti:3000  # 前端端口
lsof -ti:3001  # 后端端口

# 终止进程
kill -9 $(lsof -ti:3000)
```

</details>

<details>
<summary>翻译功能不工作</summary>

1. 检查网络连接
2. 验证API密钥配置
3. 查看后端日志：`server/backend.log`
4. 尝试使用本地翻译模型

</details>

<details>
<summary>本地模型加载失败</summary>

```bash
# 清理缓存重新下载
rm -rf ~/.cache/huggingface/
python -c "from transformers import pipeline; pipeline('translation', model='helsinki-nlp/opus-mt-en-zh')"
```

</details>

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [React](https://reactjs.org/) - 用户界面库
- [Tailwind CSS](https://tailwindcss.com/) - CSS框架
- [Hugging Face](https://huggingface.co/) - 机器学习模型
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) - 多语言翻译模型

## 📞 联系我们

- **GitHub Issues**: [提交问题](https://github.com/your-username/multilingual-forum/issues)
- **Email**: your-email@example.com
- **Discord**: [加入我们的社区](https://discord.gg/your-invite)

---

<div align="center">

**[⬆ 回到顶部](#-多语言ai论坛--multilingual-ai-forum)**

Made with ❤️ for global communication

</div> 