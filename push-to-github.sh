#!/bin/bash

echo "🚀 准备推送多语言AI论坛到GitHub..."

# 检查Git配置
echo "📋 检查Git配置..."
git config user.name "Atomheart-Father"
git config user.email "$(git config user.email)"

# 显示当前状态
echo "📊 当前Git状态:"
git status --short

# 推送到GitHub
echo "🌐 推送到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 成功推送到GitHub！"
    echo ""
    echo "📱 你的项目现在可以访问："
    echo "   GitHub仓库: https://github.com/Atomheart-Father/multilingual-forum"
    echo "   克隆命令: git clone https://github.com/Atomheart-Father/multilingual-forum.git"
    echo ""
    echo "🚀 下一步部署建议："
    echo "   1. 前端部署到Vercel: https://vercel.com"
    echo "   2. 后端部署到Railway: https://railway.app"
    echo "   3. 查看部署指南: docs/github-setup.md"
    echo ""
else
    echo "❌ 推送失败！请检查："
    echo "   1. 是否已在GitHub创建 'multilingual-forum' 仓库？"
    echo "   2. 是否有推送权限？"
    echo "   3. 网络连接是否正常？"
fi 