from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
import os
from collections import defaultdict, deque
from typing import Dict, Deque

class RateLimitMiddleware(BaseHTTPMiddleware):
    """基于内存的速率限制中间件"""
    
    def __init__(self, app, max_requests: int = 1000, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests or int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
        self.window_seconds = window_seconds or int(os.getenv("RATE_LIMIT_WINDOW_MS", "900000")) // 1000
        self.request_times: Dict[str, Deque[float]] = defaultdict(deque)
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP地址"""
        # 检查代理头部
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # 从连接信息获取
        if request.client and hasattr(request.client, 'host'):
            return request.client.host
        
        return "unknown"
    
    def _cleanup_old_requests(self, client_ip: str, current_time: float):
        """清理过期的请求记录"""
        cutoff_time = current_time - self.window_seconds
        
        while (self.request_times[client_ip] and 
               self.request_times[client_ip][0] < cutoff_time):
            self.request_times[client_ip].popleft()
    
    def _is_rate_limited(self, client_ip: str) -> bool:
        """检查是否超过速率限制"""
        current_time = time.time()
        
        # 清理过期记录
        self._cleanup_old_requests(client_ip, current_time)
        
        # 检查当前请求数
        if len(self.request_times[client_ip]) >= self.max_requests:
            return True
        
        # 记录当前请求
        self.request_times[client_ip].append(current_time)
        return False
    
    async def dispatch(self, request: Request, call_next):
        """处理请求的中间件方法"""
        # 跳过健康检查和静态文件
        if request.url.path in ["/api/health", "/health"]:
            return await call_next(request)
        
        if request.url.path.startswith("/static/"):
            return await call_next(request)
        
        client_ip = self._get_client_ip(request)
        
        # 检查速率限制
        if self._is_rate_limited(client_ip):
            return Response(
                content='{"error": "Too many requests, please try again later."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": str(self.window_seconds),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Window": str(self.window_seconds)
                }
            )
        
        # 继续处理请求
        response = await call_next(request)
        
        # 添加速率限制头部信息
        remaining_requests = max(0, self.max_requests - len(self.request_times[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining_requests)
        response.headers["X-RateLimit-Window"] = str(self.window_seconds)
        
        return response 