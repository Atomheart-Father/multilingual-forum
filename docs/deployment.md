# 🚀 部署指南

## 本地开发环境

### 1. 环境要求
- Node.js 16+
- npm 或 yarn
- Git

### 2. 快速启动
```bash
# 克隆项目
git clone https://github.com/your-username/multilingual-forum.git
cd multilingual-forum

# 安装依赖
npm run install-all

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加您的API密钥

# 启动开发服务器
npm run dev
```

## GitHub Pages 部署（免费）

### 1. 准备工作
```bash
# 安装 gh-pages
npm install --save-dev gh-pages

# 在 client/package.json 中添加
{
  "homepage": "https://your-username.github.io/multilingual-forum",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

### 2. 部署前端
```bash
cd client
npm run deploy
```

**注意**: GitHub Pages只能部署静态文件，需要配置后端API服务。

## Vercel 部署（推荐）

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 部署
```bash
# 在项目根目录
vercel

# 按照提示配置
# - Framework: Other
# - Root Directory: ./
# - Build Command: npm run build
# - Output Directory: client/build
```

### 3. 环境变量配置
在 Vercel 控制台中添加环境变量：
- `OPENAI_API_KEY`
- `AZURE_TRANSLATE_KEY`
- `GOOGLE_TRANSLATE_KEY`
- `DEEPL_API_KEY`

## Docker 部署

### 1. 构建和运行
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 2. 生产环境配置
```bash
# 生产环境启动
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 云服务器部署

### 1. AWS EC2
```bash
# 连接到服务器
ssh -i your-key.pem ubuntu@your-ec2-ip

# 安装 Docker
sudo apt update
sudo apt install docker.io docker-compose

# 克隆项目
git clone https://github.com/your-username/multilingual-forum.git
cd multilingual-forum

# 配置环境变量
cp .env.example .env
sudo nano .env

# 启动服务
sudo docker-compose up -d
```

### 2. 配置域名和 SSL
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Kubernetes 部署（企业级）

### 1. 创建 Kubernetes 配置
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multilingual-forum
spec:
  replicas: 3
  selector:
    matchLabels:
      app: multilingual-forum
  template:
    metadata:
      labels:
        app: multilingual-forum
    spec:
      containers:
      - name: server
        image: your-registry/multilingual-forum:latest
        ports:
        - containerPort: 3001
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
```

### 2. 部署到集群
```bash
# 应用配置
kubectl apply -f k8s/

# 查看状态
kubectl get pods
kubectl get services
```

## 性能优化

### 1. 缓存配置
```javascript
// server/middleware/cache.js
const redis = require('redis');
const client = redis.createClient();

const cacheTranslation = (key, translation, ttl = 3600) => {
  client.setex(key, ttl, JSON.stringify(translation));
};
```

### 2. CDN 配置
- 静态资源使用 CloudFlare CDN
- 图片使用 AWS S3 + CloudFront
- API 响应启用 gzip 压缩

### 3. 数据库优化
```javascript
// 创建索引
db.posts.createIndex({ "timestamp": -1 });
db.posts.createIndex({ "language": 1 });
db.posts.createIndex({ "author": 1 });
```

## 监控和日志

### 1. 应用监控
```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start server/index.js --name "multilingual-forum"

# 监控
pm2 monit
```

### 2. 错误追踪
```javascript
// 集成 Sentry
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});
```

## 安全考虑

### 1. API 速率限制
```javascript
// 已在项目中实现
const rateLimiter = new RateLimiterMemory({
  points: 100,
  duration: 900, // 15 minutes
});
```

### 2. HTTPS 强制
```nginx
# nginx 配置
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. 环境变量安全
- 使用 Docker secrets
- 云服务商的密钥管理服务
- 定期轮换 API 密钥

## 故障排除

### 常见问题

1. **翻译API调用失败**
   ```bash
   # 检查API密钥
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

2. **内存不足**
   ```bash
   # 增加 Node.js 内存限制
   node --max-old-space-size=4096 server/index.js
   ```

3. **端口冲突**
   ```bash
   # 查看端口使用
   netstat -tulpn | grep :3001
   ```

### 日志查看
```bash
# Docker 容器日志
docker-compose logs server

# PM2 日志
pm2 logs multilingual-forum

# 系统日志
sudo journalctl -u your-service-name
```

## 备份策略

### 1. 数据库备份
```bash
# MongoDB 备份
mongodump --host localhost:27017 --db multilingual-forum --out backup/

# 恢复
mongorestore --host localhost:27017 --db multilingual-forum backup/multilingual-forum/
```

### 2. 应用备份
```bash
# 代码备份到 Git
git push origin main

# 配置文件备份
tar -czf config-backup.tar.gz .env docker-compose.yml nginx.conf
```

这个部署指南涵盖了从开发到生产的各个环节，根据您的需求选择合适的部署方式。 