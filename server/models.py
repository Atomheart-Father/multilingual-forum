from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class LanguageCode(str, Enum):
    """支持的语言代码"""
    ZH = "zh"
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    RU = "ru"
    JA = "ja"
    KO = "ko"
    AR = "ar"
    HI = "hi"
    NL = "nl"
    SV = "sv"
    DA = "da"
    NO = "no"
    FI = "fi"
    PL = "pl"
    CS = "cs"
    HU = "hu"
    TR = "tr"
    EL = "el"
    HE = "he"
    TH = "th"
    VI = "vi"
    ID = "id"

class TranslationService(str, Enum):
    """翻译服务提供商"""
    OPENAI = "openai"
    AZURE = "azure"
    GOOGLE = "google"
    DEEPL = "deepl"
    LOCAL = "local"

# 用户相关模型
class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    preferred_language: LanguageCode = LanguageCode.EN

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    preferred_language: str
    join_date: Optional[str] = None

class UserLogin(BaseModel):
    username: str

class UserPreferences(BaseModel):
    preferred_language: LanguageCode

# 帖子相关模型
class ReplyCreate(BaseModel):
    content: str
    author: str
    language: LanguageCode = LanguageCode.EN

class ReplyResponse(BaseModel):
    id: str
    content: str
    author: str
    language: str
    timestamp: str
    likes: int = 0

class PostCreate(BaseModel):
    title: str
    content: str
    author: str
    language: LanguageCode = LanguageCode.EN

class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    author: str
    language: str
    timestamp: str
    likes: int = 0
    replies: List[ReplyResponse] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class LikeAction(BaseModel):
    action: str  # "like" or "unlike"

# 翻译相关模型
class TranslationRequest(BaseModel):
    text: str
    target_lang: LanguageCode
    source_lang: Optional[LanguageCode] = None
    service: TranslationService = TranslationService.OPENAI

class TranslationResponse(BaseModel):
    translated_text: str
    service: str
    detected_language: Optional[str] = None

# 分页模型
class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 10
    language: Optional[LanguageCode] = None

class PaginationResponse(BaseModel):
    current_page: int
    total_pages: int
    total_posts: int
    has_next: bool
    has_prev: bool

class PostsResponse(BaseModel):
    posts: List[PostResponse]
    pagination: PaginationResponse

# 统计模型
class ForumStats(BaseModel):
    total_posts: int
    total_replies: int
    total_likes: int
    languages_used: int
    recent_activity: List[dict]

# 错误响应模型
class ErrorResponse(BaseModel):
    error: str
    message: Optional[str] = None

# 成功响应模型
class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None 