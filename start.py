#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌍 多语言AI论坛 - 一键启动脚本 (Python版本)
"""

import os
import sys
import time
import signal
import subprocess
import requests
from pathlib import Path

# 颜色定义
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(message, color):
    """打印带颜色的消息"""
    print(f"{color}{message}{Colors.NC}")

def check_command(command):
    """检查命令是否存在"""
    return subprocess.run(['which', command], capture_output=True).returncode == 0

class ForumLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.backend_process = None
        self.frontend_process = None
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
    
    def cleanup(self, signum=None, frame=None):
        """清理函数"""
        print_colored("\n🛑 正在停止服务...", Colors.YELLOW)
        
        if self.backend_process:
            self.backend_process.terminate()
            print_colored("✅ 后端服务器已停止", Colors.GREEN)
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print_colored("✅ 前端服务器已停止", Colors.GREEN)
        
        print_colored("🎉 所有服务已停止，感谢使用！", Colors.GREEN)
        sys.exit(0)
    
    def check_dependencies(self):
        """检查环境依赖"""
        print_colored("📋 检查环境依赖...", Colors.BLUE)
        
        # 检查Python
        if not check_command('python3'):
            print_colored("❌ 请安装Python 3", Colors.RED)
            return False
        
        # 检查虚拟环境
        venv_path = self.project_root / 'server' / 'venv'
        if not venv_path.exists():
            print_colored("⚠️  未找到虚拟环境，请先运行: cd server && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt", Colors.YELLOW)
            return False
        
        # 检查npm
        if not check_command('npm'):
            print_colored("❌ 请安装Node.js和npm", Colors.RED)
            return False
        
        print_colored("✅ 环境检查完成", Colors.GREEN)
        return True
    
    def start_backend(self):
        """启动后端服务器"""
        print_colored("🚀 启动后端服务器...", Colors.BLUE)
        
        server_dir = self.project_root / 'server'
        venv_python = server_dir / 'venv' / 'bin' / 'python'
        
        # 启动后端
        with open(server_dir / 'backend.log', 'w') as log_file:
            self.backend_process = subprocess.Popen(
                [str(venv_python), 'main.py'],
                cwd=server_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
        
        # 等待后端启动
        print_colored("⏳ 等待后端服务器启动...", Colors.YELLOW)
        time.sleep(5)
        
        # 检查后端是否启动成功
        try:
            response = requests.get('http://localhost:3001/api/health', timeout=5)
            if response.status_code == 200:
                print_colored("✅ 后端服务器启动成功 (http://localhost:3001)", Colors.GREEN)
                return True
        except requests.RequestException:
            pass
        
        print_colored("❌ 后端服务器启动失败，请检查 server/backend.log", Colors.RED)
        if self.backend_process:
            self.backend_process.terminate()
        return False
    
    def start_frontend(self):
        """启动前端服务器"""
        print_colored("🎨 启动前端服务器...", Colors.BLUE)
        
        client_dir = self.project_root / 'client'
        
        # 设置环境变量
        env = os.environ.copy()
        env['BROWSER'] = 'none'
        
        # 启动前端
        with open(client_dir / 'frontend.log', 'w') as log_file:
            self.frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=client_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                env=env
            )
        
        # 等待前端启动
        print_colored("⏳ 等待前端服务器启动...", Colors.YELLOW)
        time.sleep(10)
        
        # 检查前端是否启动成功
        try:
            response = requests.get('http://localhost:3000/', timeout=5)
            if response.status_code == 200:
                print_colored("✅ 前端服务器启动成功 (http://localhost:3000)", Colors.GREEN)
                return True
        except requests.RequestException:
            pass
        
        print_colored("❌ 前端服务器启动失败，请检查 client/frontend.log", Colors.RED)
        self.cleanup()
        return False
    
    def run(self):
        """主运行函数"""
        print_colored("🌍 启动多语言AI论坛...", Colors.BLUE)
        
        # 检查依赖
        if not self.check_dependencies():
            sys.exit(1)
        
        # 启动后端
        if not self.start_backend():
            sys.exit(1)
        
        # 启动前端
        if not self.start_frontend():
            sys.exit(1)
        
        # 显示成功信息
        print_colored("\n🎉 多语言AI论坛启动成功！", Colors.GREEN)
        print_colored("📱 前端地址: http://localhost:3000", Colors.BLUE)
        print_colored("🔧 后端API: http://localhost:3001", Colors.BLUE)
        print_colored("📚 API文档: http://localhost:3001/docs", Colors.BLUE)
        print_colored("\n💡 按 Ctrl+C 停止所有服务", Colors.YELLOW)
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

if __name__ == "__main__":
    launcher = ForumLauncher()
    launcher.run() 