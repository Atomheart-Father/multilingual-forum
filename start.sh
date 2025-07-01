#!/bin/bash

# 🌍 多语言AI论坛 - 一键启动脚本
echo "🌍 启动多语言AI论坛..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查必要的命令
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 未安装或不在PATH中${NC}"
        return 1
    fi
    return 0
}

# 清理函数
cleanup() {
    echo -e "\n${YELLOW}🛑 正在停止服务...${NC}"
    
    # 停止后端服务器
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ 后端服务器已停止${NC}"
    fi
    
    # 停止前端服务器
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ 前端服务器已停止${NC}"
    fi
    
    echo -e "${GREEN}🎉 所有服务已停止，感谢使用！${NC}"
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}📋 检查环境依赖...${NC}"

# 检查Python
if ! check_command python3; then
    echo -e "${RED}请安装Python 3${NC}"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "$PROJECT_ROOT/server/venv" ]; then
    echo -e "${YELLOW}⚠️  未找到虚拟环境，请先运行: cd server && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# 设置nvm环境（如果存在）
if [ -s "$HOME/.nvm/nvm.sh" ]; then
    echo -e "${BLUE}🔧 加载NVM环境...${NC}"
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# 检查npm
if ! check_command npm; then
    echo -e "${RED}请安装Node.js和npm${NC}"
    exit 1
fi

# 检查前端依赖
if [ ! -d "$PROJECT_ROOT/client/node_modules" ]; then
    echo -e "${YELLOW}📦 安装前端依赖...${NC}"
    cd "$PROJECT_ROOT/client"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 前端依赖安装失败${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ 环境检查完成${NC}"

# 启动后端服务器
echo -e "${BLUE}🚀 启动后端服务器...${NC}"
cd "$PROJECT_ROOT/server"

# 激活虚拟环境并启动后端
source venv/bin/activate
python main.py > backend.log 2>&1 &
BACKEND_PID=$!

# 等待后端启动
echo -e "${YELLOW}⏳ 等待后端服务器启动...${NC}"
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:3001/api/health > /dev/null; then
    echo -e "${GREEN}✅ 后端服务器启动成功 (http://localhost:3001)${NC}"
else
    echo -e "${RED}❌ 后端服务器启动失败，请检查 server/backend.log${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 启动前端服务器
echo -e "${BLUE}🎨 启动前端服务器...${NC}"
cd "$PROJECT_ROOT/client"

# 设置环境变量以避免自动打开浏览器
export BROWSER=none

# 启动前端
npm start > frontend.log 2>&1 &
FRONTEND_PID=$!

# 等待前端启动
echo -e "${YELLOW}⏳ 等待前端服务器启动...${NC}"
sleep 10

# 检查前端是否启动成功
if curl -s http://localhost:3000/ > /dev/null; then
    echo -e "${GREEN}✅ 前端服务器启动成功 (http://localhost:3000)${NC}"
else
    echo -e "${RED}❌ 前端服务器启动失败，请检查 client/frontend.log${NC}"
    cleanup
    exit 1
fi

echo -e "\n${GREEN}🎉 多语言AI论坛启动成功！${NC}"
echo -e "${BLUE}📱 前端地址: http://localhost:3000${NC}"
echo -e "${BLUE}🔧 后端API: http://localhost:3001${NC}"
echo -e "${BLUE}📚 API文档: http://localhost:3001/docs${NC}"
echo -e "\n${YELLOW}💡 按 Ctrl+C 停止所有服务${NC}"

# 保持脚本运行，等待用户中断
while true; do
    sleep 1
done 