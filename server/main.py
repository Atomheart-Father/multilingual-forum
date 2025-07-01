from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# 导入路由
from routes.auth import router as auth_router
from routes.posts import router as posts_router
from routes.translate import router as translate_router
from routes.users import router as users_router
from middleware.rate_limit import RateLimitMiddleware

# 加载环境变量
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("🌍 Multilingual Forum server starting up...")
    yield
    # 关闭时执行
    print("🌍 Multilingual Forum server shutting down...")

# 创建FastAPI应用
app = FastAPI(
    title="Multilingual Forum API",
    description="AI-powered multilingual forum that breaks language barriers",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置 - 支持本地开发和Vercel部署
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# 如果是生产环境且没有明确设置CORS，添加常见的Vercel模式
if os.getenv("NODE_ENV") == "production" and len(allowed_origins) == 1 and allowed_origins[0] == "http://localhost:3000":
    allowed_origins.extend([
        "https://*.vercel.app",
        "https://multilingual-forum.vercel.app"
    ])

print(f"🌐 CORS允许的源: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 添加速率限制中间件
app.add_middleware(RateLimitMiddleware)

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(posts_router, prefix="/api/posts", tags=["posts"])
app.include_router(translate_router, prefix="/api/translate", tags=["translation"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

# 健康检查端点
@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    import time
    import psutil
    
    return {
        "status": "OK",
        "timestamp": time.time(),
        "uptime": time.time() - psutil.boot_time() if hasattr(psutil, 'boot_time') else 0,
        "version": "1.0.0"
    }

# 静态文件服务（用于生产环境）
if os.path.exists("../client/build"):
    app.mount("/static", StaticFiles(directory="../client/build/static"), name="static")
    app.mount("/", StaticFiles(directory="../client/build", html=True), name="client")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("NODE_ENV") == "development" else False,
        log_level="info"
    ) 