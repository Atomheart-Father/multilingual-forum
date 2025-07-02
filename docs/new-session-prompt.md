# 🤖 新AI会话引导Prompt

> **复制以下内容给新的AI助手会话，让其快速了解项目并无缝开始工作**

---

## 项目背景简介

你好！我正在开发一个多语言AI论坛项目，需要你无缝接管之前的工作。

**项目概述**：
- **项目名称**: 多语言AI论坛 (Multilingual AI Forum)
- **用户背景**: 荷兰用户，需要解决欧洲多语言交流障碍
- **核心功能**: 用户用母语发帖，AI自动翻译给其他用户看
- **技术栈**: Python FastAPI后端 + React前端 + 多AI翻译引擎

**当前状态**：
- ✅ 项目功能完成度95%+，核心功能稳定运行
- ✅ 采用Python FastAPI后端架构，已完全替代之前的Node.js版本
- ✅ 支持OpenAI、DeepL、Azure、Google翻译 + 本地AI模型
- ✅ 完整的React前端界面，响应式设计，实时翻译功能
- ✅ 多种部署方案，包括免费云端部署方案

## 🚀 立即开始工作指南

### 第一步：快速了解项目 (5分钟)
**必读文档（按优先级）**：
1. `docs/project-status.md` - 📖 完整项目状态总结 (最重要)
2. `README.md` - 📖 项目概览和快速开始
3. `docs/features-overview.md` - 📖 详细功能说明

### 第二步：验证项目可运行 (3分钟)
```bash
# 一键启动项目
./start.sh

# 验证服务
# 后端API: http://localhost:3001/docs
# 前端界面: http://localhost:3000
# 健康检查: http://localhost:3001/api/health
```

### 第三步：了解代码结构 (5分钟)
**后端核心文件**：
- `server/main.py` - FastAPI应用入口
- `server/routes/translate.py` - 核心翻译引擎 (重点)
- `server/models.py` - 数据模型定义
- `server/routes/posts.py` - 帖子管理API

**前端核心文件**：
- `client/src/App.js` - 主应用和路由
- `client/src/components/TranslatedContent.js` - 核心翻译组件
- `client/src/components/ForumHome.js` - 论坛首页

## 🏗️ 技术架构要点

### 后端 (Python FastAPI)
```python
# 项目结构
server/
├── main.py              # FastAPI入口，异步架构
├── models.py            # Pydantic数据模型
├── routes/              # API路由模块
│   ├── translate.py     # 翻译服务集成 (核心)
│   ├── posts.py         # 帖子CRUD
│   ├── auth.py          # 用户认证
│   └── users.py         # 用户管理
└── middleware/
    └── rate_limit.py    # 速率限制
```

### 翻译系统 (核心特性)
- **多引擎支持**: OpenAI GPT, DeepL, Azure, Google, 本地模型
- **智能降级**: 主服务失败自动切换备用服务
- **本地模型**: Hugging Face Transformers + Ollama LLM
- **异步处理**: 高性能API调用
- **缓存机制**: 减少重复翻译请求

### 前端 (React)
- **组件化设计**: 可复用的翻译和UI组件
- **实时翻译**: 用户可一键切换任意语言查看内容
- **响应式UI**: Tailwind CSS，适配桌面和移动端
- **状态管理**: React Hooks管理应用状态

## 🔧 常见工作任务

### 1. 修改翻译功能
```bash
# 查看翻译核心逻辑
server/routes/translate.py

# 配置API密钥
server/.env

# 测试翻译功能
python server/test_local_translation.py
```

### 2. 修改前端界面
```bash
# 主应用
client/src/App.js

# 翻译组件
client/src/components/TranslatedContent.js

# 论坛首页
client/src/components/ForumHome.js
```

### 3. 添加新API功能
```bash
# 在routes目录添加新路由
server/routes/your_new_feature.py

# 在models.py定义数据模型
server/models.py

# 在main.py注册新路由
```

### 4. 部署项目
```bash
# 本地开发
./start.sh

# Docker部署
docker-compose up -d

# 免费云端部署
# 前端: Vercel
# 后端: Render
```

## 🎯 重要配置文件

### 环境配置 (server/.env)
```env
# AI翻译服务API密钥
OPENAI_API_KEY=your_key
DEEPL_API_KEY=your_key
GOOGLE_TRANSLATE_KEY=your_key
AZURE_TRANSLATE_KEY=your_key

# 本地模型配置
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh

# 服务器设置
PORT=3001
ALLOWED_ORIGINS=http://localhost:3000
```

### API配置 (client/src/config.js)
```javascript
const API_BASE_URL = 'http://localhost:3001';
```

## 📊 项目状态指标

### 功能完成度
- ✅ 翻译系统: 100% (多引擎 + 本地模型)
- ✅ 帖子系统: 95% (发帖、回复、点赞、搜索)
- ✅ 用户系统: 90% (认证、偏好设置)
- ✅ 界面系统: 95% (响应式、实时翻译)
- ✅ 部署方案: 100% (多种部署方式)

### 支持的语言 (30+种)
- 欧洲语言: 英语、德语、法语、西班牙语、意大利语、荷兰语等
- 亚洲语言: 中文(简/繁)、日语、韩语、印地语、泰语等
- 其他语言: 阿拉伯语、土耳其语、希伯来语等

## 🐛 常见问题快速解决

### 启动问题
```bash
# 端口占用
lsof -ti:3000 3001 | xargs kill -9

# 依赖安装
cd server && pip install -r requirements.txt
cd client && npm install
```

### 翻译服务问题
1. 检查API密钥配置: `server/.env`
2. 查看错误日志: `server/backend.log`
3. 测试本地翻译: `python server/test_local_translation.py`
4. 系统会自动降级到其他可用服务

## 🎯 用户背景信息

**用户特点**：
- 位于荷兰，关注欧洲多语言交流
- 更熟悉Python，不太懂JavaScript
- 希望有免费或低成本的部署方案
- 重视数据隐私（本地模型支持）

**已满足的需求**：
- ✅ Python后端实现
- ✅ 多AI翻译引擎支持
- ✅ 本地模型隐私保护
- ✅ 免费部署方案
- ✅ 欧洲语言优化（DeepL集成）

## 📚 完整文档参考

如需深入了解，按需查看：
- `docs/changelog.md` - 项目演进历史
- `docs/deployment.md` - 部署详细指南
- `docs/api-documentation.md` - API详细文档
- `docs/new-session-guide.md` - 新会话工作指导

## 🚀 开始工作检查清单

请在开始工作前确认：
- [ ] 已阅读 `docs/project-status.md` 了解项目全貌
- [ ] 运行 `./start.sh` 确认项目可以正常启动
- [ ] 访问 `http://localhost:3001/docs` 确认API文档正常
- [ ] 访问 `http://localhost:3000` 确认前端界面正常
- [ ] 了解用户当前的具体需求和优先级

---

**🎯 目标**: 你应该能在15分钟内完全理解项目状态并开始有效工作。项目已经95%完成，功能稳定，你可以专注于用户的新需求或优化现有功能。

**💡 提示**: 如果用户提出新需求，先查看现有代码结构，保持一致的架构风格。项目采用现代化的异步Python架构，代码质量很高，可以直接基于现有框架扩展。

祝工作顺利！🎉 