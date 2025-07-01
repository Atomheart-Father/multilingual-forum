# API 文档

## 基础信息

- **基础URL**: `http://localhost:3001/api`
- **认证**: 目前使用简单的用户名认证（演示版本）
- **内容类型**: `application/json`
- **响应格式**: JSON

## 认证相关 API

### POST /api/auth/login
用户登录

**请求体**:
```json
{
  "username": "string"
}
```

**响应**:
```json
{
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "preferredLanguage": "string"
  },
  "token": "string"
}
```

### GET /api/auth/me
获取当前用户信息

**请求头**:
```
x-user-id: user_id
```

**响应**:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "preferredLanguage": "string"
}
```

### PUT /api/auth/preferences
更新用户偏好设置

**请求头**:
```
x-user-id: user_id
```

**请求体**:
```json
{
  "preferredLanguage": "string"
}
```

## 帖子相关 API

### GET /api/posts
获取帖子列表

**查询参数**:
- `page` (number): 页码，默认为1
- `limit` (number): 每页数量，默认为10
- `language` (string): 按语言过滤

**响应**:
```json
{
  "posts": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "author": "string",
      "language": "string",
      "timestamp": "string",
      "likes": "number",
      "replies": []
    }
  ],
  "pagination": {
    "currentPage": "number",
    "totalPages": "number",
    "totalPosts": "number",
    "hasNext": "boolean",
    "hasPrev": "boolean"
  }
}
```

### GET /api/posts/:id
获取特定帖子

**响应**:
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "author": "string",
  "language": "string",
  "timestamp": "string",
  "likes": "number",
  "replies": [
    {
      "id": "string",
      "content": "string",
      "author": "string",
      "language": "string",
      "timestamp": "string",
      "likes": "number"
    }
  ]
}
```

### POST /api/posts
创建新帖子

**请求体**:
```json
{
  "title": "string",
  "content": "string",
  "author": "string",
  "language": "string"
}
```

**响应**:
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "author": "string",
  "language": "string",
  "timestamp": "string",
  "likes": "number",
  "replies": []
}
```

### PUT /api/posts/:id/like
点赞/取消点赞帖子

**请求体**:
```json
{
  "action": "like" | "unlike"
}
```

**响应**:
```json
{
  "likes": "number"
}
```

### POST /api/posts/:id/reply
回复帖子

**请求体**:
```json
{
  "content": "string",
  "author": "string",
  "language": "string"
}
```

**响应**:
```json
{
  "id": "string",
  "content": "string",
  "author": "string",
  "language": "string",
  "timestamp": "string",
  "likes": "number"
}
```

### DELETE /api/posts/:id
删除帖子（管理员功能）

**响应**:
```json
{
  "message": "Post deleted successfully"
}
```

### GET /api/posts/stats/summary
获取论坛统计信息

**响应**:
```json
{
  "totalPosts": "number",
  "totalReplies": "number",
  "totalLikes": "number",
  "languagesUsed": "number",
  "recentActivity": [
    {
      "id": "string",
      "title": "string",
      "author": "string",
      "timestamp": "string"
    }
  ]
}
```

## 翻译相关 API

### POST /api/translate
翻译文本

**请求体**:
```json
{
  "text": "string",
  "targetLang": "string",
  "sourceLang": "string", // 可选，默认为 "auto"
  "service": "string" // 可选，默认为 "openai"
}
```

**响应**:
```json
{
  "translatedText": "string",
  "service": "string",
  "detectedLanguage": "string"
}
```

### GET /api/translate/languages
获取支持的语言列表

**响应**:
```json
{
  "zh": "Chinese (Simplified)",
  "en": "English",
  "es": "Spanish",
  "fr": "French",
  "de": "German",
  // ... 更多语言
}
```

## 用户相关 API

### GET /api/users
获取用户列表

**响应**:
```json
[
  {
    "id": "string",
    "username": "string",
    "preferredLanguage": "string",
    "joinDate": "string"
  }
]
```

### GET /api/users/:id
获取特定用户信息

**响应**:
```json
{
  "id": "string",
  "username": "string",
  "preferredLanguage": "string",
  "joinDate": "string"
}
```

## 系统相关 API

### GET /api/health
健康检查

**响应**:
```json
{
  "status": "OK",
  "timestamp": "string",
  "uptime": "number"
}
```

## 错误处理

所有API在发生错误时会返回以下格式：

```json
{
  "error": "错误消息",
  "message": "详细错误信息" // 可选
}
```

常见HTTP状态码：
- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权
- `404`: 资源不存在
- `429`: 请求频率限制
- `500`: 服务器内部错误

## 速率限制

- 每个IP地址每15分钟最多100个请求
- 超过限制会返回429状态码

## 翻译服务

支持的翻译服务：
1. **OpenAI** (openai) - 默认，高质量上下文翻译
2. **Azure Translator** (azure) - 快速专业翻译
3. **Google Translate** (google) - 支持语言最多
4. **DeepL** (deepl) - 欧洲语言翻译质量最佳

服务会自动降级：如果主要服务失败，会尝试备用服务。 