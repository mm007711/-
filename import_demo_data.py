#!/usr/bin/env python3
"""
演示数据导入脚本
用于将demo_class_data.json中的数据导入到111.html系统中
"""

import json
import os
import sys
from pathlib import Path

def main():
    """主函数"""
    print("=" * 50)
    print("    CodeEdu 演示数据导入工具")
    print("=" * 50)
    print()
    
    # 1. 检查演示数据文件
    data_file = Path("demo_class_data.json")
    if not data_file.exists():
        print(f"❌ 错误: 找不到演示数据文件 {data_file}")
        print(f"   请确保 demo_class_data.json 文件存在")
        return 1
    
    # 2. 加载演示数据
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ 演示数据加载成功:")
        print(f"   📊 班级数据: {len(data.get('classes', []))} 个班级")
        for cls in data.get('classes', []):
            print(f"      - {cls['name']}: {len(cls.get('students', []))} 名学生")
        
        print(f"   🏆 比赛数据: {len(data.get('contests', []))} 场比赛")
        for contest in data.get('contests', []):
            print(f"      - {contest['title']}: {contest['status']}")
        
        print(f"   📝 题目数据: {len(data.get('problems', {}))} 道题目")
        for pid, problem in data.get('problems', {}).items():
            print(f"      - No.{pid} {problem['title']}: {problem['difficulty']}")
        
        print()
        
    except Exception as e:
        print(f"❌ 加载演示数据失败: {e}")
        return 1
    
    # 3. 显示导入说明
    print("📋 导入说明:")
    print("=" * 40)
    print("""
方法1: 通过111.html界面导入
--------------------------------
1. 双击打开 111.html 文件
2. 切换到"教师/管理员"视角
3. 点击"导入/发布题目JSON"按钮
4. 选择 demo_class_data.json 文件
5. 点击"保存并导入"

方法2: 使用启动脚本
--------------------------------
Windows用户: 双击运行 start_app.bat
Linux/Mac用户: 运行 ./start_app.sh

方法3: 手动启动
--------------------------------
1. 启动后端服务器:
   python backend/simple_server.py
   
2. 在浏览器中打开:
   111.html 或 http://localhost:5173
""")
    
    # 4. 创建启动脚本
    create_start_scripts()
    
    # 5. 显示演示指南
    print()
    print("🎯 演示功能指南:")
    print("=" * 40)
    print("""
1. 多班级管理演示
   • 创建新班级
   • 切换不同班级
   • 查看学生数据

2. 批量操作演示
   • 批量选择学生
   • 批量移除学生
   • 分页浏览功能

3. 可视化图表演示
   • 成绩分布柱状图
   • 活跃度趋势折线图
   • 图表刷新功能

4. 专业报告演示
   • 生成班级分析报告
   • 打印报告功能
   • 数据导出功能

5. 比赛管理演示
   • 查看现有比赛
   • 创建新比赛
   • 题目组卷功能
""")
    
    print()
    print("✅ 演示数据准备完成！")
    print("   现在可以开始给领导演示了 🎬")
    print()
    
    return 0

def create_start_scripts():
    """创建启动脚本"""
    print()
    print("🚀 创建启动脚本...")
    
    # Windows批处理脚本
    windows_script = """@echo off
chcp 65001 >nul
echo ========================================
echo    CodeEdu 在线编程教学平台
echo ========================================
echo.
echo 📅 版本: 1.0.0
echo 🎯 用途: 教学演示与评估
echo.
echo 🚀 正在启动系统...
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.8+
    echo.
    echo 💡 解决方案:
    echo   1. 访问 https://www.python.org/downloads/
    echo   2. 下载并安装Python 3.8+
    echo   3. 安装时勾选"Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM 启动后端服务器
echo 🔧 启动后端服务器...
start /B python backend\\simple_server.py

REM 等待服务器启动
timeout /t 2 /nobreak >nul

REM 打开前端页面
echo 🌐 打开教学平台...
start "" "111.html"

echo.
echo ✅ 系统启动完成！
echo.
echo 📋 使用说明:
echo   1. 首次使用请切换到"教师/管理员"视角
echo   2. 点击"导入/发布题目JSON"
echo   3. 选择demo_class_data.json导入演示数据
echo.
echo 🎯 演示功能:
echo   • 多班级管理
echo   • 可视化图表
echo   • 批量操作
echo   • 专业报告生成
echo.
echo ⚠️  注意: 关闭此窗口将停止后端服务器
echo.
pause
"""
    
    # Linux/Mac Shell脚本
    linux_script = """#!/bin/bash

echo "========================================"
echo "   CodeEdu 在线编程教学平台"
echo "========================================"
echo ""
echo "📅 版本: 1.0.0"
echo "🎯 用途: 教学演示与评估"
echo ""
echo "🚀 正在启动系统..."
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到Python3，请先安装Python 3.8+"
    echo ""
    echo "💡 解决方案:"
    echo "   1. 访问 https://www.python.org/downloads/"
    echo "   2. 下载并安装Python 3.8+"
    echo ""
    exit 1
fi

# 启动后端服务器
echo "🔧 启动后端服务器..."
python3 backend/simple_server.py &
SERVER_PID=$!

# 等待服务器启动
sleep 2

# 打开前端页面
echo "🌐 打开教学平台..."
if command -v xdg-open &> /dev/null; then
    xdg-open "111.html"
elif command -v open &> /dev/null; then
    open "111.html"
else
    echo "请在浏览器中打开: 111.html"
fi

echo ""
echo "✅ 系统启动完成！"
echo ""
echo "📋 使用说明:"
echo "   1. 首次使用请切换到'教师/管理员'视角"
echo "   2. 点击'导入/发布题目JSON'"
echo "   3. 选择demo_class_data.json导入演示数据"
echo ""
echo "🎯 演示功能:"
echo "   • 多班级管理"
echo "   • 可视化图表"
echo "   • 批量操作"
echo "   • 专业报告生成"
echo ""
echo "⚠️  注意: 按 Ctrl+C 停止服务器"
echo ""

# 等待用户中断
wait $SERVER_PID
"""
    
    # 写入Windows脚本
    try:
        with open("start_app.bat", "w", encoding="utf-8") as f:
            f.write(windows_script)
        print("   ✅ 创建 start_app.bat (Windows启动脚本)")
    except Exception as e:
        print(f"   ❌ 创建Windows脚本失败: {e}")
    
    # 写入Linux/Mac脚本
    try:
        with open("start_app.sh", "w", encoding="utf-8") as f:
            f.write(linux_script)
        
        # 设置执行权限
        if sys.platform != "win32":
            os.chmod("start_app.sh", 0o755)
        
        print("   ✅ 创建 start_app.sh (Linux/Mac启动脚本)")
    except Exception as e:
        print(f"   ❌ 创建Linux/Mac脚本失败: {e}")
    
    print()
    print("📁 文件清单:")
    print("   • demo_class_data.json - 演示数据")
    print("   • 111.html - 主应用文件")
    print("   • start_app.bat - Windows启动脚本")
    print("   • start_app.sh - Linux/Mac启动脚本")
    print("   • import_demo_data.py - 本导入工具")

if __name__ == "__main__":
    sys.exit(main())
