#!/usr/bin/env python3
"""
测试本地翻译功能的脚本
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_local_translation():
    """测试本地翻译功能"""
    
    try:
        from routes.translate import TranslationService
        
        # 创建翻译服务实例
        service = TranslationService()
        
        print("🧪 Testing Local Translation Service")
        print("=" * 50)
        
        # 测试文本
        test_texts = [
            ("Hello, world!", "zh", "en"),
            ("你好，世界！", "en", "zh"),
            ("Bonjour le monde!", "zh", "fr"),
            ("Hola mundo!", "en", "es")
        ]
        
        for text, target_lang, source_lang in test_texts:
            print(f"\n📝 Testing: '{text}' ({source_lang} -> {target_lang})")
            
            try:
                # 测试本地翻译
                result = await service._translate_with_local_model(text, target_lang, source_lang)
                
                print(f"✅ Result: {result['translated_text']}")
                print(f"🔧 Service: {result['service']}")
                print(f"🔍 Detected: {result['detected_language']}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
                # 如果本地模型不可用，给出安装提示
                if "not available" in str(e):
                    print("\n💡 Tip: To use local models, install dependencies:")
                    print("pip install torch transformers")
                    print("or set up a local model server")
        
        print("\n" + "=" * 50)
        print("🔧 Local Model Configuration:")
        print(f"Model Type: {os.getenv('LOCAL_MODEL_TYPE', 'transformers')}")
        print(f"Model Name: {os.getenv('LOCAL_MODEL_NAME', 'helsinki-nlp/opus-mt-en-zh')}")
        print(f"Server URL: {os.getenv('LOCAL_MODEL_SERVER_URL', 'Not configured')}")
        
    except Exception as e:
        print(f"❌ Failed to import translation service: {e}")
        return False
    
    return True

async def test_translation_api():
    """测试翻译API端点"""
    
    print("\n🌐 Testing Translation API")
    print("=" * 50)
    
    try:
        import httpx
        
        # 测试数据
        test_data = {
            "text": "Hello, this is a test!",
            "target_lang": "zh",
            "source_lang": "en",
            "service": "local"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://localhost:3001/api/translate/",
                    json=test_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ API Response: {result}")
                else:
                    print(f"❌ API Error: {response.status_code} - {response.text}")
                    
            except httpx.ConnectError:
                print("❌ Cannot connect to server. Make sure the server is running:")
                print("cd server && python run.py")
                
            except Exception as e:
                print(f"❌ API Test Error: {e}")
                
    except ImportError:
        print("❌ httpx not installed. Install with: pip install httpx")

def main():
    """主函数"""
    print("🤖 Local Translation Testing Tool")
    print("=" * 50)
    
    # 设置测试环境变量
    if not os.getenv("LOCAL_MODEL_TYPE"):
        os.environ["LOCAL_MODEL_TYPE"] = "transformers"
    if not os.getenv("LOCAL_MODEL_NAME"):
        os.environ["LOCAL_MODEL_NAME"] = "helsinki-nlp/opus-mt-en-zh"
    
    # 运行测试
    asyncio.run(test_local_translation())
    asyncio.run(test_translation_api())

if __name__ == "__main__":
    main() 