from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import httpx
from typing import Dict, Any
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 优先使用简化的模型，避免复杂依赖
try:
    from models_simple import (
        TranslationRequest, 
        TranslationResponse, 
        TranslationService,
        LanguageCode,
        PostCreate, 
        PostResponse
    )
    logger.info("✅ 使用简化模型 (models_simple.py)")
except ImportError:
    try:
        from models import (
            TranslationRequest, 
            TranslationResponse, 
            TranslationService,
            LanguageCode,
            PostCreate, 
            PostResponse
        )
        logger.info("⚠️ 使用完整模型 (models.py)")
    except ImportError:
        logger.error("❌ 无法导入任何模型文件")
        raise

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Multilingual Forum API",
    description="AI-powered multilingual forum - Ultra Lightweight Version",
    version="1.0.0-simple"
)

# CORS配置
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# 添加通用的Vercel域名支持
allowed_origins.extend([
    "https://*.vercel.app",
    "https://multilingual-forum.vercel.app"
])

logger.info(f"🌐 CORS允许的源: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在云端部署时使用通配符
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 内存存储 (简化版)
posts_db = []
translations_cache = {}

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    logger.info("🚀 Multilingual Forum API (简化版) 启动中...")
    logger.info("💾 使用内存存储")
    logger.info("🔧 纯Python实现，无C扩展依赖")

@app.get("/")
async def root():
    return {
        "message": "🌍 Multilingual Forum API is running!",
        "version": "1.0.0-simple",
        "features": ["posts", "translation", "health-check"],
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "OK",
        "timestamp": time.time(),
        "version": "1.0.0-simple",
        "posts_count": len(posts_db)
    }

@app.get("/api/translate/languages")
async def get_supported_languages():
    """获取支持的语言列表"""
    return {
        "zh": "Chinese (Simplified)",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi"
    }

@app.post("/api/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """翻译文本 - 简化版，支持基本翻译或返回原文"""
    
    # 检查缓存
    cache_key = f"{request.text}_{request.target_lang}_{request.service}"
    if cache_key in translations_cache:
        return translations_cache[cache_key]
    
    # 简化的翻译实现
    try:
        # 如果有OpenAI API密钥，尝试使用OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and request.service == TranslationService.OPENAI:
            result = await translate_with_openai(request.text, request.target_lang, openai_key)
        else:
            # 返回原文作为fallback
            result = {
                "translated_text": f"[{request.target_lang.upper()}] {request.text}",
                "service": "fallback",
                "detected_language": request.source_lang.value if request.source_lang else "auto"
            }
        
        # 缓存结果
        translations_cache[cache_key] = result
        return TranslationResponse(**result)
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        # 错误时返回原文
        return TranslationResponse(
            translated_text=request.text,
            service="error_fallback",
            detected_language="unknown"
        )

async def translate_with_openai(text: str, target_lang: str, api_key: str) -> Dict[str, Any]:
    """使用OpenAI进行翻译"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"Translate to {target_lang}. Only return the translation."
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                translated_text = data["choices"][0]["message"]["content"].strip()
                return {
                    "translated_text": translated_text,
                    "service": "openai",
                    "detected_language": "auto"
                }
            else:
                raise Exception(f"OpenAI API error: {response.status_code}")
                
    except Exception as e:
        logger.error(f"OpenAI translation failed: {str(e)}")
        raise

@app.get("/api/posts/")
async def get_posts():
    """获取帖子列表"""
    return {"posts": posts_db, "total": len(posts_db)}

@app.post("/api/posts/", response_model=PostResponse)
async def create_post(post: PostCreate):
    """创建新帖子"""
    new_post = {
        "id": str(len(posts_db) + 1),
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "language": post.language.value,
        "timestamp": str(int(time.time())),
        "likes": 0
    }
    posts_db.append(new_post)
    return PostResponse(**new_post)

@app.get("/api/posts/{post_id}")
async def get_post(post_id: str):
    """获取特定帖子"""
    for post in posts_db:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    uvicorn.run(
        "main-simple:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    ) 