#!/usr/bin/env python3
"""
🧪 测试回复和点赞功能
验证新添加的API端点是否正常工作
"""

import json
import time
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
    print(f"{color}{message}{Colors.RESET}")

def make_request(url, method='GET', data=None, timeout=15):
    """发送HTTP请求"""
    try:
        req = Request(url, method=method)
        req.add_header('User-Agent', 'Forum-Test/1.0')
        req.add_header('Content-Type', 'application/json')
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urlopen(req, timeout=timeout) as response:
            return {
                'status_code': response.getcode(),
                'body': json.loads(response.read().decode('utf-8'))
            }
    except HTTPError as e:
        return {
            'status_code': e.code,
            'body': {'error': str(e)}
        }
    except Exception as e:
        raise Exception(f"请求错误: {str(e)}")

def test_reply_functionality():
    """测试回复功能"""
    log("\n💬 测试回复功能...", Colors.BLUE)
    
    base_url = "https://multilingual-forum-api.onrender.com"
    
    try:
        # 1. 获取现有帖子
        posts_response = make_request(f"{base_url}/api/posts/")
        if posts_response['status_code'] != 200:
            log("❌ 无法获取帖子列表", Colors.RED)
            return False
        
        posts = posts_response['body']['posts']
        if not posts:
            log("⚠️  没有可用的帖子进行测试", Colors.YELLOW)
            return False
        
        test_post = posts[0]
        post_id = test_post['id']
        log(f"   测试帖子: {test_post['title'][:50]}...", Colors.CYAN)
        
        # 2. 发送回复
        reply_data = {
            "content": f"这是一个测试回复 - {int(time.time())}",
            "author": "TestUser",
            "language": "zh"
        }
        
        reply_response = make_request(
            f"{base_url}/api/posts/{post_id}/reply",
            method='POST',
            data=reply_data
        )
        
        if reply_response['status_code'] == 200:
            log("   ✅ 回复发送成功", Colors.GREEN)
            reply = reply_response['body']
            log(f"   回复ID: {reply['id']}", Colors.CYAN)
            log(f"   回复内容: {reply['content'][:30]}...", Colors.CYAN)
            return True
        else:
            log(f"   ❌ 回复失败: {reply_response['status_code']}", Colors.RED)
            log(f"   错误: {reply_response['body']}", Colors.RED)
            return False
            
    except Exception as e:
        log(f"   ❌ 回复测试异常: {e}", Colors.RED)
        return False

def test_like_functionality():
    """测试点赞功能"""
    log("\n❤️ 测试点赞功能...", Colors.BLUE)
    
    base_url = "https://multilingual-forum-api.onrender.com"
    
    try:
        # 1. 获取现有帖子
        posts_response = make_request(f"{base_url}/api/posts/")
        if posts_response['status_code'] != 200:
            log("❌ 无法获取帖子列表", Colors.RED)
            return False
        
        posts = posts_response['body']['posts']
        if not posts:
            log("⚠️  没有可用的帖子进行测试", Colors.YELLOW)
            return False
        
        test_post = posts[0]
        post_id = test_post['id']
        original_likes = test_post.get('likes', 0)
        log(f"   测试帖子: {test_post['title'][:50]}...", Colors.CYAN)
        log(f"   当前点赞数: {original_likes}", Colors.CYAN)
        
        # 2. 点赞
        like_response = make_request(
            f"{base_url}/api/posts/{post_id}/like",
            method='PUT',
            data={"action": "like"}
        )
        
        if like_response['status_code'] == 200:
            new_likes = like_response['body']['likes']
            log(f"   ✅ 点赞成功，新点赞数: {new_likes}", Colors.GREEN)
            
            # 3. 取消点赞
            unlike_response = make_request(
                f"{base_url}/api/posts/{post_id}/like",
                method='PUT',
                data={"action": "unlike"}
            )
            
            if unlike_response['status_code'] == 200:
                final_likes = unlike_response['body']['likes']
                log(f"   ✅ 取消点赞成功，最终点赞数: {final_likes}", Colors.GREEN)
                return True
            else:
                log(f"   ⚠️  取消点赞失败: {unlike_response['status_code']}", Colors.YELLOW)
                return False
        else:
            log(f"   ❌ 点赞失败: {like_response['status_code']}", Colors.RED)
            log(f"   错误: {like_response['body']}", Colors.RED)
            return False
            
    except Exception as e:
        log(f"   ❌ 点赞测试异常: {e}", Colors.RED)
        return False

def test_post_with_replies():
    """测试获取包含回复的帖子"""
    log("\n📝 测试获取帖子详情（包含回复）...", Colors.BLUE)
    
    base_url = "https://multilingual-forum-api.onrender.com"
    
    try:
        # 获取帖子列表
        posts_response = make_request(f"{base_url}/api/posts/")
        if posts_response['status_code'] != 200:
            return False
        
        posts = posts_response['body']['posts']
        if not posts:
            return False
        
        # 获取第一个帖子的详细信息
        post_id = posts[0]['id']
        post_response = make_request(f"{base_url}/api/posts/{post_id}")
        
        if post_response['status_code'] == 200:
            post = post_response['body']
            log("   ✅ 帖子获取成功", Colors.GREEN)
            log(f"   帖子标题: {post['title']}", Colors.CYAN)
            log(f"   点赞数: {post.get('likes', 0)}", Colors.CYAN)
            log(f"   回复数: {len(post.get('replies', []))}", Colors.CYAN)
            
            # 显示回复
            replies = post.get('replies', [])
            if replies:
                log("   📝 回复列表:", Colors.CYAN)
                for i, reply in enumerate(replies[-3:]):  # 显示最后3条回复
                    log(f"     {i+1}. {reply['author']}: {reply['content'][:50]}...", Colors.CYAN)
            
            return True
        else:
            log(f"   ❌ 获取帖子失败: {post_response['status_code']}", Colors.RED)
            return False
            
    except Exception as e:
        log(f"   ❌ 获取帖子异常: {e}", Colors.RED)
        return False

def main():
    """主测试函数"""
    log("🧪 开始测试回复和点赞功能...", Colors.YELLOW)
    log("=" * 50, Colors.YELLOW)
    
    results = {
        'reply': test_reply_functionality(),
        'like': test_like_functionality(),
        'post_details': test_post_with_replies()
    }
    
    # 输出测试结果
    log("\n📊 测试结果汇总:", Colors.YELLOW)
    log("=" * 50, Colors.YELLOW)
    
    log(f"💬 回复功能: {'✅ 正常' if results['reply'] else '❌ 异常'}", 
        Colors.GREEN if results['reply'] else Colors.RED)
    log(f"❤️ 点赞功能: {'✅ 正常' if results['like'] else '❌ 异常'}", 
        Colors.GREEN if results['like'] else Colors.RED)
    log(f"📝 帖子详情: {'✅ 正常' if results['post_details'] else '❌ 异常'}", 
        Colors.GREEN if results['post_details'] else Colors.RED)
    
    all_passed = all(results.values())
    
    if all_passed:
        log("\n🎉 所有功能测试通过！回复和点赞功能正常工作", Colors.GREEN)
        log("👉 现在可以在前端正常使用回复和点赞功能了", Colors.CYAN)
    else:
        log("\n⚠️  部分功能测试失败", Colors.YELLOW)
        log("🔧 请检查后端API实现或网络连接", Colors.CYAN)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        log("\n⏹️  测试被用户中断", Colors.YELLOW)
        exit(1)
    except Exception as e:
        log(f"\n💥 测试过程发生错误: {e}", Colors.RED)
        exit(1) 