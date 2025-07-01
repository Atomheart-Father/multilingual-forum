# 🚀 GitHub设置和部署指南

本指南将帮助你把多语言AI论坛项目部署到GitHub，并设置自动化部署。

## 📚 目录

1. [准备工作](#准备工作)
2. [创建GitHub仓库](#创建github仓库)
3. [推送代码](#推送代码)
4. [设置GitHub Pages](#设置github-pages)
5. [配置自动化部署](#配置自动化部署)
6. [部署到云平台](#部署到云平台)
7. [环境变量配置](#环境变量配置)
8. [常见问题](#常见问题)

## 🎯 准备工作

### 1. 安装必要工具

确保你已经安装了：

```bash
# 检查Git版本
git --version

# 检查GitHub CLI (可选但推荐)
gh --version

# 如果没有安装GitHub CLI
# macOS: brew install gh
# Windows: winget install GitHub.cli
# Ubuntu: sudo apt install gh
```

### 2. 配置Git

```bash
# 设置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认分支名
git config --global init.defaultBranch main
```

## 📦 创建GitHub仓库

### 方法1: 使用GitHub CLI (推荐)

```bash
# 在项目根目录运行
cd /path/to/your/multilingual-forum

# 登录GitHub
gh auth login

# 创建GitHub仓库
gh repo create multilingual-forum --public --description "AI-powered multilingual forum breaking language barriers"

# 设置远程仓库
git remote add origin https://github.com/YOUR_USERNAME/multilingual-forum.git
```

### 方法2: 使用GitHub网站

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角的 `+` 按钮，选择 `New repository`
3. 填写仓库信息：
   - **Repository name**: `multilingual-forum`
   - **Description**: `AI-powered multilingual forum breaking language barriers`
   - **Visibility**: Public (推荐) 或 Private
   - 不要勾选 "Add a README file"（我们已经有了）
4. 点击 `Create repository`

## 📤 推送代码

### 1. 初始化Git仓库

```bash
# 如果还没有初始化Git
git init

# 添加所有文件
git add .

# 创建首次提交
git commit -m "🎉 初始提交: 多语言AI论坛项目

✨ 特性:
- Python FastAPI 后端
- React 前端
- 本地AI翻译模型支持
- 36+种语言支持
- 完整的论坛功能"
```

### 2. 连接远程仓库

```bash
# 添加远程仓库 (如果使用方法2创建的仓库)
git remote add origin https://github.com/YOUR_USERNAME/multilingual-forum.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 🌐 设置GitHub Pages

由于这个项目包含后端，GitHub Pages只能托管前端部分。推荐使用专门的部署平台。

### 选项1: 仅前端到GitHub Pages

如果你想只把前端部署到GitHub Pages：

1. 在GitHub仓库页面，点击 `Settings`
2. 滚动到 `Pages` 部分
3. 在 `Source` 下选择 `GitHub Actions`
4. 创建前端部署工作流：

```yaml
# .github/workflows/frontend-pages.yml
name: Deploy Frontend to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: client/package-lock.json
      
      - name: Install dependencies
        run: |
          cd client
          npm ci
      
      - name: Build
        run: |
          cd client
          npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./client/build
```

## 🔄 配置自动化部署

### 1. 设置GitHub Secrets

在GitHub仓库页面：

1. 点击 `Settings` -> `Secrets and variables` -> `Actions`
2. 点击 `New repository secret`
3. 添加以下密钥：

| 密钥名称 | 说明 | 示例值 |
|---------|------|--------|
| `DOCKER_USERNAME` | Docker Hub用户名 | `your_dockerhub_username` |
| `DOCKER_PASSWORD` | Docker Hub密码或访问令牌 | `your_dockerhub_password` |
| `VERCEL_TOKEN` | Vercel部署令牌 | `vercel_token_here` |
| `ORG_ID` | Vercel组织ID | `team_xxx` |
| `PROJECT_ID` | Vercel项目ID | `prj_xxx` |
| `RAILWAY_TOKEN` | Railway部署令牌 | `railway_token_here` |

### 2. 获取部署令牌

#### Vercel令牌
```bash
# 安装Vercel CLI
npm i -g vercel

# 登录并获取令牌
vercel login
vercel --help
```

#### Railway令牌
1. 访问 [Railway](https://railway.app)
2. 在设置中生成API令牌

## ☁️ 部署到云平台

### 推荐部署方案

1. **前端**: Vercel (免费，自动化，完美支持React)
2. **后端**: Railway (简单易用) 或 Render (免费层)

### Vercel部署前端

1. 访问 [Vercel](https://vercel.com)
2. 连接GitHub账户
3. 选择你的仓库
4. 配置项目：
   - **Framework Preset**: Create React App
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. 点击Deploy

### Railway部署后端

1. 访问 [Railway](https://railway.app)
2. 连接GitHub账户
3. 选择你的仓库
4. Railway会自动检测到Python项目
5. 设置环境变量
6. 部署

### Render部署后端

1. 访问 [Render](https://render.com)
2. 连接GitHub账户
3. 创建新的Web Service
4. 选择你的仓库
5. 配置：
   - **Environment**: Python 3
   - **Build Command**: `cd server && pip install -r requirements.txt`
   - **Start Command**: `cd server && python main.py`

## ⚙️ 环境变量配置

### 1. 复制示例配置

```bash
# 在server目录下
cp env.example .env
```

### 2. 编辑环境变量

```bash
# 编辑.env文件
nano server/.env
```

### 3. 云平台环境变量

在部署平台（Vercel、Railway、Render）的控制台中设置：

#### 必需的环境变量：
- `PORT=3001`
- `ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app`

#### 可选的翻译API密钥：
- `OPENAI_API_KEY`
- `DEEPL_API_KEY`
- `AZURE_TRANSLATE_KEY`
- `GOOGLE_TRANSLATE_KEY`

#### 本地模型配置：
- `LOCAL_MODEL_TYPE=transformers`
- `LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh`

## 🔗 连接前后端

### 1. 更新前端API地址

在 `client/src/App.js` 中更新API基础URL：

```javascript
// 开发环境
const API_BASE_URL = 'http://localhost:3001';

// 生产环境
const API_BASE_URL = 'https://your-backend-domain.railway.app';

// 或者使用环境变量
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';
```

### 2. 设置前端环境变量

在Vercel中设置：
- `REACT_APP_API_URL=https://your-backend-domain.railway.app`

## 🐛 常见问题

### Q: GitHub Actions构建失败

**A**: 检查以下几点：
1. 确保所有必需的secrets已设置
2. 检查Node.js和Python版本是否正确
3. 确保`package.json`和`requirements.txt`文件存在
4. 查看GitHub Actions日志获取详细错误信息

### Q: 部署后前端无法连接后端

**A**: 
1. 检查CORS配置：确保后端允许前端域名
2. 检查API URL：确保前端使用正确的后端URL
3. 检查网络：后端是否正常运行

### Q: 翻译功能不工作

**A**:
1. 检查API密钥是否正确设置
2. 尝试使用本地翻译模型
3. 检查网络连接和API配额

### Q: 本地模型加载失败

**A**:
```bash
# 清理Hugging Face缓存
rm -rf ~/.cache/huggingface/

# 重新下载模型
python -c "from transformers import pipeline; pipeline('translation', model='helsinki-nlp/opus-mt-en-zh')"
```

## 📊 监控和分析

### 1. 添加Google Analytics (可选)

在 `client/public/index.html` 中添加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

### 2. 错误监控 (可选)

添加Sentry进行错误追踪：

```bash
cd client
npm install @sentry/react @sentry/tracing
```

## 🚀 完成部署！

完成以上步骤后，你的多语言AI论坛就成功部署到GitHub了！

### 最终URLs:
- **GitHub仓库**: `https://github.com/YOUR_USERNAME/multilingual-forum`
- **前端应用**: `https://your-project.vercel.app`
- **后端API**: `https://your-project.railway.app`
- **API文档**: `https://your-project.railway.app/docs`

### 下一步：
1. 在README中更新实际的部署链接
2. 设置自定义域名（可选）
3. 配置SSL证书（通常自动配置）
4. 监控应用性能和错误

祝贺你！🎉 你的多语言AI论坛现在已经在线并可以全球访问了！ 