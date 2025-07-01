#!/usr/bin/env python3
"""
多语言论坛后端启动脚本
"""

import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    """启动服务器"""
    port = int(os.getenv("PORT", 3001))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌍 Starting Multilingual Forum on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("NODE_ENV") == "development",
        log_level="info"
    )

if __name__ == "__main__":
    main() 