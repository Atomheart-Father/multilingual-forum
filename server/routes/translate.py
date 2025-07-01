from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import Dict, Any
from models import TranslationRequest, TranslationResponse, LanguageCode
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TranslationService:
    """翻译服务类，支持多个翻译提供商"""
    
    def __init__(self):
        self.services = {
            "openai": self._translate_with_openai,
            "azure": self._translate_with_azure,
            "google": self._translate_with_google,
            "deepl": self._translate_with_deepl,
            "local": self._translate_with_local_model
        }
    
    async def _translate_with_openai(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """使用OpenAI进行翻译"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": f"You are a professional translator. Translate the following text to {target_lang}. Maintain the original tone and context. Only return the translated text, no explanations."
                            },
                            {
                                "role": "user",
                                "content": text
                            }
                        ],
                        "max_tokens": 1000,
                        "temperature": 0.3
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    translated_text = data["choices"][0]["message"]["content"].strip()
                    return {
                        "translated_text": translated_text,
                        "service": "openai",
                        "detected_language": "unknown"
                    }
                else:
                    error_data = response.json()
                    raise Exception(f"OpenAI API error: {error_data.get('error', {}).get('message', 'Unknown error')}")
                    
        except Exception as e:
            logger.error(f"OpenAI translation failed: {str(e)}")
            raise Exception(f"OpenAI translation failed: {str(e)}")
    
    async def _translate_with_azure(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """使用Azure Translator进行翻译"""
        api_key = os.getenv("AZURE_TRANSLATE_KEY")
        region = os.getenv("AZURE_TRANSLATE_REGION", "eastus")
        
        if not api_key:
            raise Exception("Azure Translator API key not configured")
        
        try:
            params = {
                "api-version": "3.0",
                "to": target_lang
            }
            if source_lang != "auto":
                params["from"] = source_lang
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.cognitive.microsofttranslator.com/translate",
                    headers={
                        "Ocp-Apim-Subscription-Key": api_key,
                        "Ocp-Apim-Subscription-Region": region,
                        "Content-Type": "application/json"
                    },
                    params=params,
                    json=[{"text": text}]
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data[0]
                    return {
                        "translated_text": result["translations"][0]["text"],
                        "service": "azure",
                        "detected_language": result.get("detectedLanguage", {}).get("language", "unknown")
                    }
                else:
                    error_data = response.json()
                    raise Exception(f"Azure translation failed: {error_data.get('error', {}).get('message', 'Unknown error')}")
                    
        except Exception as e:
            logger.error(f"Azure translation failed: {str(e)}")
            raise Exception(f"Azure translation failed: {str(e)}")
    
    async def _translate_with_google(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """使用Google Translate进行翻译"""
        api_key = os.getenv("GOOGLE_TRANSLATE_KEY")
        if not api_key:
            raise Exception("Google Translate API key not configured")
        
        try:
            data = {
                "q": text,
                "target": target_lang
            }
            if source_lang != "auto":
                data["source"] = source_lang
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://translation.googleapis.com/language/translate/v2",
                    headers={"Content-Type": "application/json"},
                    params={"key": api_key},
                    json=data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data["data"]["translations"][0]
                    return {
                        "translated_text": result["translatedText"],
                        "service": "google",
                        "detected_language": result.get("detectedSourceLanguage", "unknown")
                    }
                else:
                    error_data = response.json()
                    raise Exception(f"Google translation failed: {error_data.get('error', {}).get('message', 'Unknown error')}")
                    
        except Exception as e:
            logger.error(f"Google translation failed: {str(e)}")
            raise Exception(f"Google translation failed: {str(e)}")
    
    async def _translate_with_deepl(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """使用DeepL进行翻译"""
        api_key = os.getenv("DEEPL_API_KEY")
        if not api_key:
            raise Exception("DeepL API key not configured")
        
        try:
            data = {
                "text": [text],
                "target_lang": target_lang.upper()
            }
            if source_lang != "auto":
                data["source_lang"] = source_lang.upper()
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api-free.deepl.com/v2/translate",
                    headers={
                        "Authorization": f"DeepL-Auth-Key {api_key}",
                        "Content-Type": "application/json"
                    },
                    json=data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data["translations"][0]
                    return {
                        "translated_text": result["text"],
                        "service": "deepl",
                        "detected_language": result.get("detected_source_language", "unknown").lower()
                    }
                else:
                    error_data = response.json()
                    raise Exception(f"DeepL translation failed: {error_data.get('message', 'Unknown error')}")
                    
        except Exception as e:
            logger.error(f"DeepL translation failed: {str(e)}")
            raise Exception(f"DeepL translation failed: {str(e)}")
    
    async def translate(self, text: str, target_lang: str, source_lang: str = "auto", preferred_service: str = "openai") -> Dict[str, Any]:
        """执行翻译，支持服务降级"""
        service_func = self.services.get(preferred_service)
        if not service_func:
            raise HTTPException(status_code=400, detail=f"Unsupported translation service: {preferred_service}")
        
        try:
            return await service_func(text, target_lang, source_lang)
        except Exception as e:
            logger.error(f"Primary service {preferred_service} failed: {str(e)}")
            
            # 尝试备用服务
            fallback_services = [s for s in self.services.keys() if s != preferred_service]
            
            for fallback_service in fallback_services:
                try:
                    logger.info(f"Trying fallback service: {fallback_service}")
                    return await self.services[fallback_service](text, target_lang, source_lang)
                except Exception as fallback_error:
                    logger.error(f"Fallback service {fallback_service} failed: {str(fallback_error)}")
            
            raise HTTPException(status_code=500, detail="All translation services failed")
    
    async def _translate_with_local_model(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """使用本地部署的翻译模型进行翻译"""
        try:
            # 检查本地模型配置
            local_model_type = os.getenv("LOCAL_MODEL_TYPE", "transformers")
            model_name = os.getenv("LOCAL_MODEL_NAME", "helsinki-nlp/opus-mt-en-zh")
            model_server_url = os.getenv("LOCAL_MODEL_SERVER_URL")
            
            if model_server_url:
                # 使用本地模型服务器API
                return await self._translate_with_local_server(text, target_lang, source_lang, model_server_url)
            else:
                # 使用本地加载的模型
                return await self._translate_with_local_transformers(text, target_lang, source_lang, local_model_type, model_name)
                
        except Exception as e:
            logger.error(f"Local model translation failed: {str(e)}")
            raise Exception(f"Local model translation failed: {str(e)}")
    
    async def _translate_with_local_server(self, text: str, target_lang: str, source_lang: str, server_url: str) -> Dict[str, Any]:
        """使用本地模型服务器进行翻译"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{server_url}/translate",
                    json={
                        "text": text,
                        "source_lang": source_lang,
                        "target_lang": target_lang
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "translated_text": data.get("translated_text", text),
                        "service": "local_server",
                        "detected_language": data.get("detected_language", source_lang)
                    }
                else:
                    raise Exception(f"Local server error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Local server translation failed: {str(e)}")
            raise Exception(f"Local server translation failed: {str(e)}")
    
    async def _translate_with_local_transformers(self, text: str, target_lang: str, source_lang: str, model_type: str, model_name: str) -> Dict[str, Any]:
        """使用本地Transformers模型进行翻译"""
        try:
            # 这里是本地模型的实现框架
            # 需要根据具体的模型类型来实现
            
            if model_type == "transformers":
                return await self._use_huggingface_transformers(text, target_lang, source_lang, model_name)
            elif model_type == "ollama":
                return await self._use_ollama_model(text, target_lang, source_lang, model_name)
            elif model_type == "custom":
                return await self._use_custom_model(text, target_lang, source_lang, model_name)
            else:
                raise Exception(f"Unsupported local model type: {model_type}")
                
        except Exception as e:
            logger.error(f"Local transformers translation failed: {str(e)}")
            raise Exception(f"Local transformers translation failed: {str(e)}")
    
    async def _use_huggingface_transformers(self, text: str, target_lang: str, source_lang: str, model_name: str) -> Dict[str, Any]:
        """使用Hugging Face Transformers模型"""
        try:
            # 检查是否安装了transformers库
            try:
                import torch
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
                from transformers.pipelines import pipeline
            except ImportError:
                logger.warning("Transformers库未安装，降级到云端翻译服务")
                # 在云端部署时，自动降级到其他翻译服务
                for service in ["openai", "azure", "google", "deepl"]:
                    try:
                        if service in self.services:
                            logger.info(f"尝试使用{service}翻译服务作为本地模型的替代")
                            return await self.services[service](text, target_lang, source_lang)
                    except Exception as e:
                        logger.warning(f"{service}服务也不可用: {str(e)}")
                        continue
                
                # 如果所有服务都不可用，返回原文
                return {
                    "translated_text": text,
                    "service": "local_fallback",
                    "detected_language": source_lang
                }
            
            # 构建语言对模型名称
            if source_lang == "auto":
                # 简化处理，假设为英文
                source_lang = "en"
            
            # 构建模型名称 (例如: helsinki-nlp/opus-mt-en-zh)
            if model_name.startswith("helsinki-nlp/opus-mt-"):
                # 使用指定的模型
                pass
            else:
                # 自动构建模型名称
                model_name = f"helsinki-nlp/opus-mt-{source_lang}-{target_lang}"
            
            # 这里实现实际的模型加载和翻译逻辑
            # 为了避免阻塞，应该在线程池中运行
            import asyncio
            import concurrent.futures
            
            def translate_sync():
                try:
                    # 检查设备
                    device = "mps" if torch.backends.mps.is_available() else "cpu"
                    
                    # 加载模型和分词器 - 修复meta tensor问题
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    model = AutoModelForSeq2SeqLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float32,  # 指定数据类型
                        device_map=None  # 不使用自动设备映射
                    )
                    
                    # 手动将模型移动到设备
                    model = model.to(device)
                    
                    # 创建翻译管道
                    translator = pipeline(
                        "translation", 
                        model=model, 
                        tokenizer=tokenizer,
                        device=0 if device == "mps" else -1
                    )
                    
                    # 执行翻译
                    result = translator(text, max_length=512)
                    translated_text = result[0]['translation_text'] if result else text
                    
                    return translated_text
                except Exception as e:
                    logger.error(f"Transformers model error: {str(e)}")
                    return text  # 翻译失败时返回原文
            
            # 在线程池中运行同步代码
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                translated_text = await loop.run_in_executor(executor, translate_sync)
            
            return {
                "translated_text": translated_text,
                "service": "local_transformers",
                "detected_language": source_lang
            }
            
        except Exception as e:
            logger.error(f"Hugging Face transformers translation failed: {str(e)}")
            # 降级到返回原文
            return {
                "translated_text": text,
                "service": "local_transformers_fallback",
                "detected_language": source_lang
            }
    
    async def _use_ollama_model(self, text: str, target_lang: str, source_lang: str, model_name: str) -> Dict[str, Any]:
        """使用Ollama本地大语言模型进行翻译"""
        try:
            ollama_url = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")
            
            prompt = f"Translate the following text from {source_lang} to {target_lang}. Only return the translation, no explanations:\n\n{text}"
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{ollama_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "top_p": 0.9
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    translated_text = data.get("response", text).strip()
                    
                    return {
                        "translated_text": translated_text,
                        "service": "local_ollama",
                        "detected_language": source_lang
                    }
                else:
                    raise Exception(f"Ollama server error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Ollama translation failed: {str(e)}")
            raise Exception(f"Ollama translation failed: {str(e)}")
    
    async def _use_custom_model(self, text: str, target_lang: str, source_lang: str, model_name: str) -> Dict[str, Any]:
        """使用自定义模型进行翻译"""
        try:
            # 这里可以实现自定义的本地模型调用逻辑
            # 例如调用用户自己训练的模型、第三方本地服务等
            
            custom_model_path = os.getenv("CUSTOM_MODEL_PATH")
            if not custom_model_path:
                raise Exception("Custom model path not configured")
            
            # 示例：调用自定义脚本或服务
            # 实际实现需要根据具体的模型格式来定制
            
            return {
                "translated_text": f"[Custom translation: {text}]",  # 占位符
                "service": "local_custom",
                "detected_language": source_lang
            }
            
        except Exception as e:
            logger.error(f"Custom model translation failed: {str(e)}")
            raise Exception(f"Custom model translation failed: {str(e)}")

# 创建翻译服务实例
translation_service = TranslationService()

@router.post("/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """翻译文本"""
    if not request.text or not request.target_lang:
        raise HTTPException(status_code=400, detail="Missing required parameters: text and target_lang")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters allowed.")
    
    try:
        source_lang = request.source_lang.value if request.source_lang else "auto"
        result = await translation_service.translate(
            text=request.text,
            target_lang=request.target_lang.value,
            source_lang=source_lang,
            preferred_service=request.service.value
        )
        
        return TranslationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.get("/languages")
async def get_supported_languages():
    """获取支持的语言列表"""
    return {
        "zh": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
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
        "hi": "Hindi",
        "nl": "Dutch",
        "sv": "Swedish",
        "da": "Danish",
        "no": "Norwegian",
        "fi": "Finnish",
        "pl": "Polish",
        "cs": "Czech",
        "hu": "Hungarian",
        "tr": "Turkish",
        "el": "Greek",
        "he": "Hebrew",
        "th": "Thai",
        "vi": "Vietnamese",
        "id": "Indonesian",
        "ms": "Malay",
        "tl": "Filipino",
        "uk": "Ukrainian",
        "bg": "Bulgarian",
        "hr": "Croatian",
        "sr": "Serbian",
        "sl": "Slovenian",
        "sk": "Slovak",
        "ro": "Romanian",
        "et": "Estonian",
        "lv": "Latvian",
        "lt": "Lithuanian"
    } 