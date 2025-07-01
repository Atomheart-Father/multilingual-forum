#!/usr/bin/env python3
"""
简单的测试脚本，验证Python后端能否正常启动
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
    print("✅ Successfully imported FastAPI app")
    
    from routes.translate import router as translate_router
    print("✅ Successfully imported translate router")
    
    from routes.posts import router as posts_router
    print("✅ Successfully imported posts router")
    
    from routes.auth import router as auth_router
    print("✅ Successfully imported auth router")
    
    from routes.users import router as users_router
    print("✅ Successfully imported users router")
    
    from models import LanguageCode, TranslationService
    print("✅ Successfully imported data models")
    
    print("\n🌍 Python backend is ready to run!")
    print("To start the server, run: python run.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install missing dependencies:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1) 