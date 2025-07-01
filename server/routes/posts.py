from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import uuid
from models import (
    PostCreate, PostResponse, PostUpdate, ReplyCreate, ReplyResponse,
    LikeAction, PostsResponse, PaginationResponse, ForumStats
)

router = APIRouter()

# 内存存储（演示用，生产环境建议使用数据库）
posts_db = [
    {
        "id": "1",
        "title": "Welcome to the Multilingual Forum!",
        "content": "This is a revolutionary platform where people from all over the world can communicate without language barriers. Post in your native language and read in your preferred language!",
        "author": "Admin",
        "language": "en",
        "timestamp": "2024-01-01T12:00:00Z",
        "likes": 15,
        "replies": []
    },
    {
        "id": "2",
        "title": "Bonjour le monde!",
        "content": "Je suis très excité de pouvoir communiquer avec des gens du monde entier. Cette technologie va vraiment changer la façon dont nous interagissons en ligne.",
        "author": "Pierre",
        "language": "fr",
        "timestamp": "2024-01-02T10:30:00Z",
        "likes": 8,
        "replies": []
    },
    {
        "id": "3",
        "title": "¡Hola comunidad!",
        "content": "Estoy impresionado por esta plataforma. Finalmente podemos romper las barreras del idioma y conectar con personas de todo el mundo de manera más efectiva.",
        "author": "María",
        "language": "es",
        "timestamp": "2024-01-02T14:15:00Z",
        "likes": 12,
        "replies": []
    }
]

next_post_id = 4

@router.get("/", response_model=PostsResponse)
async def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    language: Optional[str] = None
):
    """获取帖子列表"""
    # 按语言过滤
    filtered_posts = posts_db
    if language:
        filtered_posts = [post for post in posts_db if post["language"] == language]
    
    # 按时间戳排序（最新的在前）
    filtered_posts.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # 分页计算
    total_posts = len(filtered_posts)
    total_pages = (total_posts + limit - 1) // limit
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = filtered_posts[start_index:end_index]
    
    # 构造分页信息
    pagination = PaginationResponse(
        current_page=page,
        total_pages=total_pages,
        total_posts=total_posts,
        has_next=end_index < total_posts,
        has_prev=start_index > 0
    )
    
    return PostsResponse(
        posts=[PostResponse(**post) for post in paginated_posts],
        pagination=pagination
    )

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    """获取特定帖子"""
    post = next((post for post in posts_db if post["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostResponse(**post)

@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    """创建新帖子"""
    global next_post_id
    
    if not post.title.strip() or not post.content.strip() or not post.author.strip():
        raise HTTPException(status_code=400, detail="Missing required fields: title, content, author")
    
    if len(post.title) > 200:
        raise HTTPException(status_code=400, detail="Title too long. Maximum 200 characters allowed.")
    
    if len(post.content) > 5000:
        raise HTTPException(status_code=400, detail="Content too long. Maximum 5000 characters allowed.")
    
    new_post = {
        "id": str(next_post_id),
        "title": post.title.strip(),
        "content": post.content.strip(),
        "author": post.author.strip(),
        "language": post.language.value,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "likes": 0,
        "replies": []
    }
    
    posts_db.insert(0, new_post)  # 添加到开头
    next_post_id += 1
    
    return PostResponse(**new_post)

@router.put("/{post_id}/like")
async def like_post(post_id: str, action: LikeAction):
    """点赞/取消点赞帖子"""
    post = next((post for post in posts_db if post["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if action.action == "like":
        post["likes"] += 1
    elif action.action == "unlike" and post["likes"] > 0:
        post["likes"] -= 1
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'like' or 'unlike'")
    
    return {"likes": post["likes"]}

@router.post("/{post_id}/reply", response_model=ReplyResponse)
async def add_reply(post_id: str, reply: ReplyCreate):
    """添加回复"""
    post = next((post for post in posts_db if post["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if not reply.content.strip() or not reply.author.strip():
        raise HTTPException(status_code=400, detail="Missing required fields: content, author")
    
    if len(reply.content) > 2000:
        raise HTTPException(status_code=400, detail="Reply too long. Maximum 2000 characters allowed.")
    
    new_reply = {
        "id": str(int(datetime.utcnow().timestamp() * 1000)),  # 简单的ID生成
        "content": reply.content.strip(),
        "author": reply.author.strip(),
        "language": reply.language.value,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "likes": 0
    }
    
    post["replies"].append(new_reply)
    
    return ReplyResponse(**new_reply)

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    """删除帖子（管理员功能）"""
    global posts_db
    
    post_index = next((i for i, post in enumerate(posts_db) if post["id"] == post_id), None)
    if post_index is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    posts_db.pop(post_index)
    
    return {"message": "Post deleted successfully"}

@router.get("/stats/summary", response_model=ForumStats)
async def get_forum_stats():
    """获取论坛统计信息"""
    total_posts = len(posts_db)
    total_replies = sum(len(post["replies"]) for post in posts_db)
    total_likes = sum(post["likes"] for post in posts_db)
    languages_used = len(set(post["language"] for post in posts_db))
    
    recent_activity = [
        {
            "id": post["id"],
            "title": post["title"],
            "author": post["author"],
            "timestamp": post["timestamp"]
        }
        for post in posts_db[:5]
    ]
    
    return ForumStats(
        total_posts=total_posts,
        total_replies=total_replies,
        total_likes=total_likes,
        languages_used=languages_used,
        recent_activity=recent_activity
    ) 