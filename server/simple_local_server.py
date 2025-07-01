#!/usr/bin/env python3
"""
简单的本地翻译模型服务器示例
可以作为LOCAL_MODEL_SERVER_URL的后端服务
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(title="Local Translation Model Server", version="1.0.0")

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: str
    model_name: str

# 模拟的翻译函数（实际应用中替换为真实的模型调用）
def simple_translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    简单的翻译函数示例
    在实际应用中，这里应该调用真正的翻译模型
    """
    
    # 简单的模拟翻译规则
    translations = {
        ("hello", "en", "zh"): "你好",
        ("world", "en", "zh"): "世界",
        ("你好", "zh", "en"): "hello",
        ("世界", "zh", "en"): "world",
        ("bonjour", "fr", "en"): "hello",
        ("monde", "fr", "en"): "world"
    }
    
    # 尝试简单的词汇翻译
    text_lower = text.lower()
    if (text_lower, source_lang, target_lang) in translations:
        return translations[(text_lower, source_lang, target_lang)]
    
    # 如果没有找到翻译，返回模拟的翻译结果
    if target_lang == "zh":
        return f"[中文翻译: {text}]"
    elif target_lang == "en":
        return f"[English translation: {text}]"
    elif target_lang == "fr":
        return f"[Traduction française: {text}]"
    else:
        return f"[Translation to {target_lang}: {text}]"

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Local Translation Model Server",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """翻译接口"""
    try:
        # 验证输入
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
        
        # 执行翻译
        translated_text = simple_translate(
            request.text, 
            request.source_lang, 
            request.target_lang
        )
        
        return TranslationResponse(
            translated_text=translated_text,
            detected_language=request.source_lang,
            model_name="simple-mock-translator-v1.0"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/models")
async def list_models():
    """列出可用的模型"""
    return {
        "models": [
            {
                "name": "simple-mock-translator",
                "version": "1.0",
                "languages": ["en", "zh", "fr"],
                "description": "Simple mock translator for testing"
            }
        ]
    }

@app.get("/languages")
async def supported_languages():
    """获取支持的语言"""
    return {
        "languages": {
            "en": "English",
            "zh": "Chinese (Simplified)",
            "fr": "French"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🤖 Starting Local Translation Model Server on port {port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"🔧 Health Check: http://localhost:{port}/health")
    print("\n💡 To use this server with the main forum:")
    print(f"   Set LOCAL_MODEL_SERVER_URL=http://localhost:{port}")
    print("   Set LOCAL_MODEL_TYPE=custom")
    
    uvicorn.run(
        "simple_local_server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    ) 