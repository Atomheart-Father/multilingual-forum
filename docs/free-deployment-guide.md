# 🆓 免费部署指南：Render + Vercel

本指南将教你如何**完全免费**地部署多语言AI论坛到云端。

## 🎯 部署架构

```
用户浏览器 
    ↓
🌐 Vercel (前端) 
    ↓ API调用
🔧 Render (后端)
    ↓
🤖 AI翻译服务
```

## 📋 第一步：部署后端到Render

### 1. 准备Render配置

在项目根目录创建Render配置：

```yaml
# render.yaml
services:
  - type: web
    name: multilingual-forum-api
    runtime: python
    plan: free
    buildCommand: cd server && pip install -r requirements.txt
    startCommand: cd server && python main.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        fromService:
          type: web
          name: multilingual-forum-api
          property: port
```

### 2. 部署到Render

1. **访问 [Render](https://render.com) 并注册**

2. **连接GitHub**：
   - 点击 "New" → "Web Service"
   - 选择 "Connect a repository"
   - 授权并选择你的 `multilingual-forum` 仓库

3. **配置服务**：
   ```
   Name: multilingual-forum-api
   Runtime: Python 3
   Build Command: cd server && pip install -r requirements.txt
   Start Command: cd server && python main.py
   Plan: Free
   ```

4. **设置环境变量**：
   ```
   PORT: (自动设置)
   ALLOWED_ORIGINS: https://your-app-name.vercel.app
   LOCAL_MODEL_TYPE: transformers
   LOCAL_MODEL_NAME: helsinki-nlp/opus-mt-en-zh
   ```

5. **点击 "Create Web Service"**

### 3. 获取后端API地址

部署成功后，你会得到类似这样的URL：
```
https://multilingual-forum-api.onrender.com
```

## 🎨 第二步：部署前端到Vercel

### 1. 更新前端API配置

创建环境变量配置：

```javascript
// client/src/config.js
const config = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:3001',
  isDevelopment: process.env.NODE_ENV === 'development'
};

export default config;
```

### 2. 更新App.js

```javascript
// client/src/App.js 顶部添加
import config from './config';

// 替换所有的 'http://localhost:3001' 为
const API_BASE_URL = config.API_BASE_URL;
```

### 3. 部署到Vercel

1. **访问 [Vercel](https://vercel.com) 并登录**

2. **导入项目**：
   - 点击 "New Project"
   - 选择你的 `multilingual-forum` 仓库

3. **配置构建设置**：
   ```
   Framework Preset: Create React App
   Root Directory: client
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **设置环境变量**：
   ```
   REACT_APP_API_URL: https://multilingual-forum-api.onrender.com
   ```

5. **点击 "Deploy"**

## 🔗 第三步：连接前后端

### 1. 更新后端CORS配置

```python
# server/main.py 更新CORS设置
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # 本地开发
    "https://your-app-name.vercel.app",  # Vercel部署
    "https://*.vercel.app",  # Vercel预览部署
]
```

### 2. 在Render环境变量中设置

```
ALLOWED_ORIGINS: https://your-app-name.vercel.app,https://*.vercel.app
```

### 3. 重新部署

提交代码更改，两个平台会自动重新部署。

## 🧪 测试部署

### 1. 测试后端API

访问：`https://multilingual-forum-api.onrender.com/docs`

应该能看到FastAPI文档页面。

### 2. 测试前端

访问：`https://your-app-name.vercel.app`

应该能正常加载论坛界面。

### 3. 测试API连接

在前端尝试发帖或翻译，检查是否能正常调用后端API。

## 🔧 常见问题解决

### Q: Render服务启动失败

**解决方案**：
1. 检查 `server/requirements.txt` 是否包含所有依赖
2. 确保 `server/main.py` 中有 `if __name__ == "__main__"` 启动代码
3. 查看Render部署日志获取具体错误

### Q: 前端无法连接后端

**解决方案**：
1. 检查Vercel环境变量是否正确设置
2. 确保后端CORS配置包含前端域名
3. 检查后端是否正常运行

### Q: Render免费层限制

**特点**：
- ✅ 完全免费
- ✅ 512MB RAM
- ✅ 自动SSL
- ❌ 15分钟无访问会休眠
- ❌ 冷启动需要30秒左右

**优化建议**：
- 使用外部监控服务定期访问保持唤醒
- 在首页添加加载提示

## 🚀 部署完成！

### 最终访问地址

- **前端应用**: `https://your-app-name.vercel.app`
- **后端API**: `https://multilingual-forum-api.onrender.com`
- **API文档**: `https://multilingual-forum-api.onrender.com/docs`

### 性能优化建议

1. **添加加载状态**：处理Render冷启动延迟
2. **缓存优化**：前端缓存翻译结果
3. **错误处理**：后端服务暂时不可用时的友好提示

## 💰 成本分析

```
Vercel前端: 免费 ✅
Render后端: 免费 ✅
AI翻译API: 本地模型免费 ✅
总成本: $0/月 🎉
```

祝贺！你现在拥有一个完全免费的在线多语言AI论坛！🎊 