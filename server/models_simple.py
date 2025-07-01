from pydantic import BaseModel
from typing import List, Optional
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

class TranslationService(str, Enum):
    """翻译服务提供商"""
    OPENAI = "openai"
    AZURE = "azure"
    GOOGLE = "google"
    DEEPL = "deepl"
    LOCAL = "local"

# 简化的用户模型
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    preferred_language: LanguageCode = LanguageCode.EN

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    preferred_language: str

# 简化的帖子模型
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

# 翻译模型
class TranslationRequest(BaseModel):
    text: str
    target_lang: LanguageCode
    source_lang: Optional[LanguageCode] = None
    service: TranslationService = TranslationService.LOCAL

class TranslationResponse(BaseModel):
    translated_text: str
    service: str
    detected_language: Optional[str] = None

# 错误响应
class ErrorResponse(BaseModel):
    error: str
    message: Optional[str] = None 