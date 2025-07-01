from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from models import UserLogin, UserResponse, UserPreferences

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

@router.post("/login")
async def login(user_login: UserLogin):
    """用户登录（简单演示版本）"""
    if not user_login.username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    # 查找现有用户
    user = next(
        (u for u in users_db if u["username"].lower() == user_login.username.lower()),
        None
    )
    
    # 如果用户不存在，创建新用户
    if not user:
        new_user = {
            "id": str(len(users_db) + 1),
            "username": user_login.username.strip(),
            "email": f"{user_login.username.strip().lower()}@example.com",
            "preferred_language": "en",
            "join_date": "2024-01-01"
        }
        users_db.append(new_user)
        user = new_user
    
    return {
        "user": UserResponse(**user),
        "token": "demo-jwt-token"  # 在真实应用中，这里应该生成真正的JWT
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(x_user_id: Optional[str] = Header(None)):
    """获取当前用户信息"""
    user_id = x_user_id or "1"  # 默认用户ID
    
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserResponse(**user)

@router.put("/preferences", response_model=UserResponse)
async def update_user_preferences(
    preferences: UserPreferences,
    x_user_id: Optional[str] = Header(None)
):
    """更新用户偏好设置"""
    user_id = x_user_id or "1"  # 默认用户ID
    
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 更新用户偏好
    user["preferred_language"] = preferences.preferred_language.value
    
    return UserResponse(**user) 