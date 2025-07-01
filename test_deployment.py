#!/usr/bin/env python3
"""
🧪 多语言论坛部署测试脚本
验证Vercel前端和Render后端的连接
"""

import json
import time
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 颜色输出
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

def log(message, color=Colors.RESET):
    """带颜色的日志输出"""
    print(f"{color}{message}{Colors.RESET}")

def make_request(url, timeout=30):
    """发送HTTP请求"""
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Multilingual-Forum-Test/1.0')
        
        with urlopen(req, timeout=timeout) as response:
            return {
                'status_code': response.getcode(),
                'headers': dict(response.headers),
                'body': response.read().decode('utf-8')
            }
    except HTTPError as e:
        return {
            'status_code': e.code,
            'headers': {},
            'body': str(e)
        }
    except URLError as e:
        raise Exception(f"连接失败: {e.reason}")
    except Exception as e:
        raise Exception(f"请求错误: {str(e)}")

def test_backend():
    """测试Render后端"""
    log("\n🔧 测试Render后端...", Colors.BLUE)
    
    backend_url = "https://multilingual-forum-api.onrender.com/api/health"
    
    try:
        response = make_request(backend_url, timeout=30)
        
        if response['status_code'] == 200:
            try:
                data = json.loads(response['body'])
                log("✅ 后端健康检查通过", Colors.GREEN)
                log(f"   状态: {data.get('status', 'unknown')}", Colors.CYAN)
                log(f"   版本: {data.get('version', 'unknown')}", Colors.CYAN)
                log(f"   Python版本: {data.get('python_version', 'unknown')}", Colors.CYAN)
                log(f"   帖子数量: {data.get('posts_count', 0)}", Colors.CYAN)
                return True
            except json.JSONDecodeError:
                log("⚠️  后端响应不是有效的JSON", Colors.YELLOW)
                log(f"   响应内容: {response['body'][:200]}...", Colors.CYAN)
                return False
        else:
            log(f"❌ 后端响应错误: {response['status_code']}", Colors.RED)
            return False
            
    except Exception as error:
        log(f"❌ 后端连接失败: {error}", Colors.RED)
        return False

def test_frontend():
    """测试Vercel前端"""
    log("\n🎨 测试Vercel前端...", Colors.BLUE)
    
    frontend_url = "https://multilingual-forum.vercel.app"
    
    try:
        response = make_request(frontend_url, timeout=15)
        
        if response['status_code'] == 200:
            log("✅ 前端访问正常", Colors.GREEN)
            log(f"   状态码: {response['status_code']}", Colors.CYAN)
            
            # 检查是否包含React应用标识
            body = response['body'].lower()
            if 'root' in body or 'react' in body or 'multilingual' in body:
                log("   ✓ React应用加载成功", Colors.CYAN)
            else:
                log("   ⚠️  页面内容可能异常", Colors.YELLOW)
            
            return True
        else:
            log(f"❌ 前端响应错误: {response['status_code']}", Colors.RED)
            return False
            
    except Exception as error:
        log(f"❌ 前端连接失败: {error}", Colors.RED)
        return False

def test_api_endpoints():
    """测试API端点"""
    log("\n🌐 测试API端点...", Colors.BLUE)
    
    endpoints = [
        {"name": "获取帖子", "path": "/api/posts/"},
        {"name": "支持语言", "path": "/api/translate/languages"}
    ]
    
    passed_tests = 0
    base_url = "https://multilingual-forum-api.onrender.com"
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint['path']}"
            response = make_request(url, timeout=20)
            
            if response['status_code'] == 200:
                log(f"   ✅ {endpoint['name']}: OK", Colors.GREEN)
                passed_tests += 1
            else:
                log(f"   ❌ {endpoint['name']}: {response['status_code']}", Colors.RED)
                
        except Exception as error:
            log(f"   ❌ {endpoint['name']}: {error}", Colors.RED)
    
    return passed_tests == len(endpoints)

def test_cors():
    """测试CORS配置"""
    log("\n🌐 测试CORS配置...", Colors.BLUE)
    
    try:
        # 模拟前端请求
        url = "https://multilingual-forum-api.onrender.com/api/health"
        req = Request(url)
        req.add_header('Origin', 'https://multilingual-forum.vercel.app')
        req.add_header('User-Agent', 'Multilingual-Forum-Test/1.0')
        
        with urlopen(req, timeout=15) as response:
            headers = dict(response.headers)
            cors_header = headers.get('Access-Control-Allow-Origin', '')
            
            if cors_header == '*' or 'vercel.app' in cors_header:
                log("   ✅ CORS配置正确", Colors.GREEN)
                return True
            else:
                log(f"   ⚠️  CORS可能有问题: {cors_header}", Colors.YELLOW)
                return False
                
    except Exception as error:
        log(f"   ❌ CORS测试失败: {error}", Colors.RED)
        return False

def main():
    """主测试函数"""
    log("🌍 多语言论坛部署测试开始...", Colors.YELLOW)
    log("=" * 50, Colors.YELLOW)
    
    results = {
        'backend': False,
        'frontend': False,
        'api': False,
        'cors': False
    }
    
    # 执行测试
    results['backend'] = test_backend()
    results['frontend'] = test_frontend()
    
    if results['backend']:
        results['api'] = test_api_endpoints()
        results['cors'] = test_cors()
    
    # 输出结果
    log("\n📊 测试结果汇总:", Colors.YELLOW)
    log("=" * 50, Colors.YELLOW)
    
    log(f"🔧 Render后端: {'✅ 正常' if results['backend'] else '❌ 异常'}", 
        Colors.GREEN if results['backend'] else Colors.RED)
    log(f"🎨 Vercel前端: {'✅ 正常' if results['frontend'] else '❌ 异常'}", 
        Colors.GREEN if results['frontend'] else Colors.RED)
    log(f"🌐 API端点: {'✅ 正常' if results['api'] else '❌ 异常'}", 
        Colors.GREEN if results['api'] else Colors.RED)
    log(f"🔗 CORS配置: {'✅ 正常' if results['cors'] else '❌ 异常'}", 
        Colors.GREEN if results['cors'] else Colors.RED)
    
    # 总结
    all_passed = all(results.values())
    
    if all_passed:
        log("\n🎉 所有测试通过！前后端协同正常工作", Colors.GREEN)
        log("👉 你可以开始使用论坛了:", Colors.CYAN)
        log("   前端: https://multilingual-forum.vercel.app", Colors.CYAN)
        log("   后端: https://multilingual-forum-api.onrender.com", Colors.CYAN)
        log("\n📝 使用建议:", Colors.BLUE)
        log("   1. 访问前端URL查看论坛界面", Colors.CYAN)
        log("   2. 尝试创建一个测试帖子", Colors.CYAN)
        log("   3. 测试多语言翻译功能", Colors.CYAN)
    else:
        log("\n⚠️  部分测试失败，请检查以下问题:", Colors.YELLOW)
        if not results['backend']:
            log("   - Render后端可能未正常启动或URL不正确", Colors.RED)
        if not results['frontend']:
            log("   - Vercel前端可能未正确部署", Colors.RED)
        if not results['api']:
            log("   - API端点可能存在问题", Colors.RED)
        if not results['cors']:
            log("   - CORS配置可能导致前后端通信问题", Colors.RED)
        
        log("\n🔧 故障排除建议:", Colors.BLUE)
        log("   1. 检查Render控制台的部署日志", Colors.CYAN)
        log("   2. 确认Vercel前端的环境变量配置", Colors.CYAN)
        log("   3. 查看浏览器开发者工具的网络请求", Colors.CYAN)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        log("\n⏹️  测试被用户中断", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        log(f"\n💥 测试过程发生错误: {e}", Colors.RED)
        sys.exit(1) 