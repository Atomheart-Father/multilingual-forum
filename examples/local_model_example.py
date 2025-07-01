#!/usr/bin/env python3
"""
本地翻译模型使用示例
演示如何在多语言论坛中使用本地翻译模型
"""

import asyncio
import os
import sys

async def test_local_translation_api():
    """测试本地翻译API接口"""
    
    print("🌍 Local Translation Model Example")
    print("=" * 50)
    
    try:
        import httpx
        
        # 假设服务器正在运行
        base_url = "http://localhost:3001"
        
        # 测试不同类型的翻译请求
        test_cases = [
            {
                "text": "Hello, this is a test of local translation!",
                "target_lang": "zh",
                "source_lang": "en",
                "service": "local",
                "description": "英文到中文"
            },
            {
                "text": "你好，这是本地翻译的测试！",
                "target_lang": "en", 
                "source_lang": "zh",
                "service": "local",
                "description": "中文到英文"
            },
            {
                "text": "Bonjour, comment allez-vous?",
                "target_lang": "en",
                "source_lang": "fr",
                "service": "local",
                "description": "法文到英文"
            }
        ]
        
        async with httpx.AsyncClient() as client:
            print(f"📡 Testing API endpoint: {base_url}/api/translate/")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n🧪 Test {i}: {test_case['description']}")
                print(f"📝 Original: {test_case['text']}")
                
                try:
                    response = await client.post(
                        f"{base_url}/api/translate/",
                        json={
                            "text": test_case["text"],
                            "target_lang": test_case["target_lang"],
                            "source_lang": test_case["source_lang"],
                            "service": test_case["service"]
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Translated: {result['translated_text']}")
                        print(f"🔧 Service: {result['service']}")
                        print(f"🔍 Detected: {result.get('detected_language', 'N/A')}")
                    else:
                        print(f"❌ Error: {response.status_code} - {response.text}")
                        
                except httpx.ConnectError:
                    print("❌ Server not running. Start with: cd server && python run.py")
                    break
                except Exception as e:
                    print(f"❌ Request failed: {e}")
    
    except ImportError:
        print("❌ httpx not installed. Install with: pip install httpx")

def show_configuration_examples():
    """展示不同配置选项的示例"""
    
    print("\n🔧 Configuration Examples")
    print("=" * 50)
    
    configs = [
        {
            "name": "Hugging Face Transformers (Helsinki-NLP)",
            "description": "轻量级，适合生产环境",
            "env": {
                "LOCAL_MODEL_TYPE": "transformers",
                "LOCAL_MODEL_NAME": "helsinki-nlp/opus-mt-en-zh"
            }
        },
        {
            "name": "Hugging Face Transformers (M2M100)",
            "description": "多语言支持，质量更高",
            "env": {
                "LOCAL_MODEL_TYPE": "transformers", 
                "LOCAL_MODEL_NAME": "facebook/m2m100_418M"
            }
        },
        {
            "name": "Ollama (本地大模型)",
            "description": "最高质量，需要GPU",
            "env": {
                "LOCAL_MODEL_TYPE": "ollama",
                "LOCAL_MODEL_NAME": "llama2:7b",
                "OLLAMA_SERVER_URL": "http://localhost:11434"
            }
        },
        {
            "name": "自定义模型服务器",
            "description": "自定义模型部署",
            "env": {
                "LOCAL_MODEL_TYPE": "custom",
                "LOCAL_MODEL_SERVER_URL": "http://localhost:8080",
                "CUSTOM_MODEL_PATH": "/path/to/your/model"
            }
        }
    ]
    
    for config in configs:
        print(f"\n📋 {config['name']}")
        print(f"   {config['description']}")
        print("   环境变量配置:")
        for key, value in config['env'].items():
            print(f"   {key}={value}")

def show_installation_guide():
    """显示安装指南"""
    
    print("\n📦 Installation Guide")
    print("=" * 50)
    
    print("1️⃣ 基础依赖 (必需):")
    print("   pip install fastapi uvicorn httpx")
    
    print("\n2️⃣ 本地模型依赖 (可选):")
    print("   # Hugging Face Transformers")
    print("   pip install torch transformers sentencepiece")
    print("   ")
    print("   # GPU支持 (推荐)")
    print("   pip install torch --index-url https://download.pytorch.org/whl/cu118")
    
    print("\n3️⃣ Ollama安装 (可选):")
    print("   # macOS")
    print("   brew install ollama")
    print("   ")
    print("   # Linux")
    print("   curl -fsSL https://ollama.ai/install.sh | sh")
    print("   ")
    print("   # 下载模型")
    print("   ollama pull llama2:7b")

def show_performance_comparison():
    """显示性能对比"""
    
    print("\n⚡ Performance Comparison")
    print("=" * 50)
    
    comparison = [
        ["Model Type", "Quality", "Speed", "Memory", "Use Case"],
        ["-" * 20, "-" * 10, "-" * 10, "-" * 10, "-" * 20],
        ["Helsinki-NLP", "中等", "快", "低", "生产环境，特定语言对"],
        ["M2M100-418M", "高", "中等", "中等", "多语言支持"],
        ["M2M100-1.2B", "很高", "慢", "高", "高质量翻译"],
        ["Ollama LLM", "最高", "很慢", "很高", "最高质量，有GPU"],
        ["OpenAI API", "很高", "中等", "无", "云端服务，按量计费"],
        ["DeepL API", "最高", "快", "无", "欧洲语言，按量计费"],
    ]
    
    for row in comparison:
        print(f"   {row[0]:<20} {row[1]:<10} {row[2]:<10} {row[3]:<10} {row[4]:<20}")

async def main():
    """主函数"""
    
    print("🤖 Multi-lingual Forum - Local Translation Example")
    print("🌍 Breaking language barriers with AI")
    print("=" * 60)
    
    # 显示配置示例
    show_configuration_examples()
    
    # 显示安装指南
    show_installation_guide()
    
    # 显示性能对比
    show_performance_comparison()
    
    # 测试API (如果服务器运行中)
    print("\n🧪 Testing Local Translation API...")
    await test_local_translation_api()
    
    print("\n" + "=" * 60)
    print("📚 More information:")
    print("   - Local Models Guide: docs/local-models.md")
    print("   - Deployment Guide: docs/deployment.md")
    print("   - API Documentation: http://localhost:3001/docs")
    print("\n🚀 Happy translating!")

if __name__ == "__main__":
    asyncio.run(main()) 