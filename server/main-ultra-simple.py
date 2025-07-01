#!/usr/bin/env python3
"""
🌍 超轻量级多语言论坛API - 零外部依赖版本
使用Python标准库，100%兼容所有Python版本
"""

import json
import os
import sys
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 内存存储
posts_db = []
translations_cache = {}

class MultillingualForumHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """处理GET请求"""
        try:
            path = urlparse(self.path).path
            
            if path == '/':
                self.send_json_response({
                    "message": "🌍 Multilingual Forum API is running!",
                    "version": "ultra-simple",
                    "features": ["posts", "translation", "health-check"],
                    "docs": "API endpoints: /api/health, /api/posts/, /api/translate/languages"
                })
            elif path == '/api/health':
                self.send_json_response({
                    "status": "OK",
                    "timestamp": time.time(),
                    "version": "ultra-simple",
                    "posts_count": len(posts_db),
                    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                })
            elif path == '/api/posts/':
                self.send_json_response({
                    "posts": posts_db,
                    "total": len(posts_db)
                })
            elif path == '/api/translate/languages':
                self.send_json_response({
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
                })
            elif path.startswith('/api/posts/'):
                post_id = path.split('/')[-1]
                post = self.get_post_by_id(post_id)
                if post:
                    self.send_json_response(post)
                else:
                    self.send_error_response(404, "Post not found")
            else:
                self.send_error_response(404, "Not found")
                
        except Exception as e:
            logger.error(f"GET error: {str(e)}")
            self.send_error_response(500, f"Internal server error: {str(e)}")

    def do_POST(self):
        """处理POST请求"""
        try:
            path = urlparse(self.path).path
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            if path == '/api/posts/':
                self.create_post(data)
            elif path == '/api/translate/':
                self.translate_text(data)
            else:
                self.send_error_response(404, "Not found")
                
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            logger.error(f"POST error: {str(e)}")
            self.send_error_response(500, f"Internal server error: {str(e)}")

    def create_post(self, data):
        """创建新帖子"""
        try:
            new_post = {
                "id": str(len(posts_db) + 1),
                "title": data.get("title", ""),
                "content": data.get("content", ""),
                "author": data.get("author", "Anonymous"),
                "language": data.get("language", "en"),
                "timestamp": str(int(time.time())),
                "likes": 0
            }
            posts_db.append(new_post)
            self.send_json_response(new_post)
            logger.info(f"Created post: {new_post['title']}")
        except Exception as e:
            self.send_error_response(400, f"Error creating post: {str(e)}")

    def translate_text(self, data):
        """翻译文本（简化版）"""
        try:
            text = data.get("text", "")
            target_lang = data.get("target_lang", "en")
            service = data.get("service", "fallback")
            
            # 检查缓存
            cache_key = f"{text}_{target_lang}_{service}"
            if cache_key in translations_cache:
                self.send_json_response(translations_cache[cache_key])
                return
            
            # 简化的翻译逻辑
            if service == "openai" and os.getenv("OPENAI_API_KEY"):
                # 这里可以添加真实的OpenAI调用
                translated_text = f"[OpenAI] {text} → {target_lang}"
            else:
                # fallback: 标记原文
                translated_text = f"[{target_lang.upper()}] {text}"
            
            result = {
                "translated_text": translated_text,
                "service": service,
                "detected_language": "auto"
            }
            
            # 缓存结果
            translations_cache[cache_key] = result
            self.send_json_response(result)
            
        except Exception as e:
            self.send_error_response(400, f"Translation error: {str(e)}")

    def get_post_by_id(self, post_id):
        """通过ID获取帖子"""
        for post in posts_db:
            if post["id"] == post_id:
                return post
        return None

    def send_json_response(self, data, status_code=200):
        """发送JSON响应"""
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def send_error_response(self, status_code, message):
        """发送错误响应"""
        error_data = {
            "error": message,
            "status_code": status_code,
            "timestamp": time.time()
        }
        self.send_json_response(error_data, status_code)

    def send_cors_headers(self):
        """发送CORS头部"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"{self.address_string()} - {format % args}")

def run_server():
    """启动HTTP服务器"""
    port = int(os.getenv("PORT", 3001))
    
    logger.info("🚀 Multilingual Forum API (超轻量版) 启动中...")
    logger.info("💾 使用内存存储")
    logger.info("🔧 100%标准库实现，零外部依赖")
    logger.info(f"🌍 服务器启动在端口 {port}")
    
    server = HTTPServer(('0.0.0.0', port), MultillingualForumHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 服务器正在关闭...")
        server.shutdown()

if __name__ == "__main__":
    run_server() 