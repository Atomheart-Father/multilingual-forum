from fastapi import APIRouter, HTTPException
from typing import List
from models import UserResponse

router = APIRouter()

# 简单的内存存储（演示用）
users_db = [
    {
        "id": "1",
        "username": "admin",
        "email": "admin@example.com",
        "preferred_language": "en",
        "join_date": "2024-01-01"
    },
    {
        "id": "2",
        "username": "pierre",
        "email": "pierre@example.com",
        "preferred_language": "fr",
        "join_date": "2024-01-02"
    },
    {
        "id": "3",
        "username": "maria",
        "email": "maria@example.com",
        "preferred_language": "es",
        "join_date": "2024-01-02"
    }
]

@router.get("/", response_model=List[UserResponse])
async def get_users():
    """获取用户列表（演示用）"""
    return [UserResponse(**user) for user in users_db]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """获取特定用户信息"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user) 