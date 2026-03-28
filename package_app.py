#!/usr/bin/env python3
"""
CodeEdu 应用打包脚本
将前端和后端打包成便携式软件
"""

import os
import shutil
import zipfile
import json
from pathlib import Path
import sys

def create_portable_package():
    """创建便携式软件包"""
    print("=" * 60)
    print("      CodeEdu 教学平台 - 便携版打包工具")
    print("=" * 60)
    print()
    
    # 创建打包目录
    package_name = "CodeEdu_Portable_v1.0"
    package_dir = Path(package_name)
    
    if package_dir.exists():
        print(f"[!] 检测到已存在的打包目录: {package_dir}")
        print("   自动删除并重新创建...")
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    print(f"[OK] 创建打包目录: {package_dir}")
    print()
    
    # 1. 复制核心文件
    print("[文件] 复制核心文件...")
    core_files = [
        "111.html",
        "demo_class_data.json",
        "import_demo_data.py",
        "demo-mode-simple.js",
        "demo-mode.js",
        "demo.html",
        "DEMO_GUIDE.md",
        "CLASS_MANAGEMENT_OPTIMIZATION_SUMMARY.md",
        "FUNCTIONALITY_VERIFICATION_REPORT.md"
    ]
    
    copied_count = 0
    for file in core_files:
        src = Path(file)
        if src.exists():
            dst = package_dir / file
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"   [OK] {file}")
            copied_count += 1
        else:
            print(f"   [!] {file} (未找到)")
    
    print(f"   已复制 {copied_count}/{len(core_files)} 个核心文件")
    print()
    
    # 2. 复制后端文件
    print("[工具] 复制后端文件...")
    backend_dir = package_dir / "backend"
    backend_dir.mkdir()
    
    backend_files = [
        "backend/simple_server.py",
        "backend/main.py",
        "backend/models.py",
        "backend/database.py",
        "backend/judge.py",
        "backend/schemas.py",
        "backend/init_test_data_simple.py",
        "backend/test_api.py"
    ]
    
    backend_copied = 0
    for file in backend_files:
        src = Path(file)
        if src.exists():
            dst = package_dir / file
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"   [OK] {file}")
            backend_copied += 1
        else:
            print(f"   [!] {file} (未找到)")
    
    print(f"   已复制 {backend_copied}/{len(backend_files)} 个后端文件")
    print()
    
    # 3. 创建启动脚本
    print("[启动] 创建启动脚本...")
    
    # Windows启动脚本
    windows_launcher = package_dir / "启动教学平台.bat"
    windows_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo    CodeEdu 在线编程教学平台 - 便携版
echo ========================================
echo.
echo [版本] 1.0.0
echo [打包] 2025-03-26
echo [用途] 教学演示与评估
echo [支持] 计算机学院
echo.
echo [启动] 正在启动系统...
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python
    echo.
    echo [提示] 解决方案:
    echo   1. 访问 https://www.python.org/downloads/
    echo   2. 下载并安装Python 3.8+
    echo   3. 安装时勾选"Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [服务] 启动后端服务器...
start /B python backend\\simple_server.py

echo [等待] 等待服务器启动...
timeout /t 3 /nobreak >nul

echo [前端] 打开教学平台...
start "" "111.html"

echo.
echo [成功] 系统启动成功！
echo.
echo [说明] 使用说明:
echo   1. 首次使用请切换到"教师/管理员"视角
echo   2. 点击"导入/发布题目JSON"
echo   3. 选择demo_class_data.json导入演示数据
echo.
echo [功能] 演示功能:
echo   - 多班级管理系统
echo   - 可视化统计图表
echo   - 批量操作功能
echo   - 专业报告生成
echo   - 比赛/测验管理
echo   - 在线编程判题
echo.
echo [数据] 演示数据:
echo   - 2个班级，20名学生
echo   - 2场比赛，3道题目
echo   - 完整成绩和活跃度数据
echo.
echo [注意] 关闭此窗口将停止后端服务器
echo.
echo [演示] 现在可以开始给领导演示了！
echo.
pause
'''
    
    with open(windows_launcher, 'w', encoding='utf-8') as f:
        f.write(windows_content)
    print("   [OK] 启动教学平台.bat (Windows启动脚本)")
    
    # Linux/Mac启动脚本
    linux_launcher = package_dir / "启动教学平台.sh"
    linux_content = '''#!/bin/bash

echo "========================================"
echo "   CodeEdu 在线编程教学平台 - 便携版"
echo "========================================"
echo ""
echo "[版本] 1.0.0"
echo "[打包] 2025-03-26"
echo "[用途] 教学演示与评估"
echo "[支持] 计算机学院"
echo ""
echo "[启动] 正在启动系统..."
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3"
    echo ""
    echo "[提示] 解决方案:"
    echo "   1. 访问 https://www.python.org/downloads/"
    echo "   2. 下载并安装Python 3.8+"
    echo ""
    exit 1
fi

echo "[服务] 启动后端服务器..."
python3 backend/simple_server.py &
SERVER_PID=$!

echo "[等待] 等待服务器启动..."
sleep 3

echo "[前端] 打开教学平台..."
if command -v xdg-open &> /dev/null; then
    xdg-open "111.html"
elif command -v open &> /dev/null; then
    open "111.html"
else
    echo "请在浏览器中打开: 111.html"
fi

echo ""
echo "[成功] 系统启动成功！"
echo ""
echo "[说明] 使用说明:"
echo "   1. 首次使用请切换到'教师/管理员'视角"
echo "   2. 点击'导入/发布题目JSON'"
echo "   3. 选择demo_class_data.json导入演示数据"
echo ""
echo "[功能] 演示功能:"
echo "   - 多班级管理系统"
echo "   - 可视化统计图表"
echo "   - 批量操作功能"
echo "   - 专业报告生成"
echo "   - 比赛/测验管理"
echo "   - 在线编程判题"
echo ""
echo "[数据] 演示数据:"
echo "   - 2个班级，20名学生"
echo "   - 2场比赛，3道题目"
echo "   - 完整成绩和活跃度数据"
echo ""
echo "[注意] 按 Ctrl+C 停止服务器"
echo ""
echo "[演示] 现在可以开始给领导演示了！"
echo ""

# 等待用户中断
wait $SERVER_PID
'''
    
    with open(linux_launcher, 'w', encoding='utf-8') as f:
        f.write(linux_content)
    
    # 设置执行权限
    os.chmod(linux_launcher, 0o755)
    print("   [OK] 启动教学平台.sh (Linux/Mac启动脚本)")
    print()
    
    # 4. 创建配置文件
    print("[配置] 创建配置文件...")
    config = {
        "app_name": "CodeEdu在线编程教学平台",
        "version": "1.0.0",
        "build_date": "2025-03-26",
        "developer": "计算机学院",
        "description": "功能完整的在线编程教学平台，支持多班级管理、可视化分析、批量操作、专业报告生成等功能",
        "features": [
            "多班级管理系统",
            "可视化统计图表",
            "批量操作功能",
            "专业报告生成",
            "比赛/测验管理",
            "在线编程判题",
            "数据导入导出",
            "演示模式支持"
        ],
        "system_requirements": {
            "python": ">=3.8",
            "browser": "Chrome 90+, Firefox 88+, Edge 90+",
            "os": "Windows 10+, macOS 10.15+, Linux",
            "memory": "4GB+",
            "storage": "100MB+"
        },
        "demo_data": {
            "classes": 2,
            "students": 20,
            "contests": 2,
            "problems": 3,
            "total_score_records": 20,
            "total_submissions": 400
        },
        "export_formats": ["CSV", "JSON", "PDF"],
        "supported_languages": ["Python", "JavaScript"],
        "contact": {
            "department": "计算机学院",
            "purpose": "教学演示与评估"
        }
    }
    
    config_file = package_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("   [OK] config.json (配置文件)")
    print()
    
    # 5. 创建说明文档
    print("[文档] 创建说明文档...")
    readme_content = f"""# CodeEdu 在线编程教学平台 - 便携版 v1.0

## 平台简介

CodeEdu 是一个功能完整的在线编程教学平台，专为计算机教育设计。平台集成了多班级管理、可视化数据分析、批量操作、专业报告生成等核心功能，适合教学演示、课堂使用和领导评估。

## 快速开始

### Windows 用户
1. 双击运行 `启动教学平台.bat`
2. 系统会自动启动后端服务器
3. 浏览器会自动打开教学平台界面

### Linux/Mac 用户
1. 打开终端
2. 运行命令: `./启动教学平台.sh`
3. 系统会自动启动后端服务器
4. 浏览器会自动打开教学平台界面

## 核心功能演示

### 1. 多班级管理系统 [OK]
- **创建/编辑/删除**多个班级
- **一键切换**不同班级
- **学生数据**独立存储
- **班级统计**实时更新

### 2. 可视化统计图表 [OK]
- **成绩分布**柱状图
- **活跃度趋势**折线图
- **实时刷新**功能
- **响应式**设计

### 3. 批量操作功能 [OK]
- **批量选择**学生
- **批量移除**操作
- **分页浏览**支持
- **状态提示**显示

### 4. 专业报告生成 [OK]
- **一键生成**班级分析报告
- **打印支持**功能
- **专业格式**输出
- **数据导出**CSV/JSON

### 5. 比赛/测验管理 [OK]
- **创建编程**比赛
- **题目组卷**功能
- **比赛状态**管理
- **参与统计**显示

### 6. 在线编程判题 [OK]
- **支持Python/JavaScript**
- **实时代码**执行
- **自动判题**评分
- **测试用例**管理

## 演示指南

### 第一步: 导入演示数据
1. 打开平台后，切换到"**教师/管理员**"视角
2. 点击"**导入/发布题目JSON**"按钮
3. 选择 `demo_class_data.json` 文件
4. 点击"**保存并导入**"

### 第二步: 体验核心功能
1. **班级管理演示**: 创建新班级，切换不同班级
2. **批量操作演示**: 勾选学生，尝试批量移除
3. **可视化演示**: 查看成绩分布和活跃度趋势
4. **报告生成演示**: 点击"生成报告"查看专业分析
5. **比赛管理演示**: 查看现有比赛，尝试创建新比赛

### 第三步: 导出功能演示
1. 在班级管理页面，点击"**导出成绩单**"
2. 系统会自动下载**CSV文件**
3. 用**Excel**打开查看导出数据

## 系统要求

### 软件要求
- **Python**: 3.8 或更高版本 (必需)
- **浏览器**: Chrome 90+, Firefox 88+, Edge 90+
- **操作系统**: Windows 10+, macOS 10.15+, Linux

### 硬件要求
- **内存**: 4GB 或更多
- **存储**: 100MB 可用空间
- **网络**: 本地运行，无需互联网

## 文件结构

```
{package_name}/
├── 启动教学平台.bat              # Windows启动脚本
├── 启动教学平台.sh               # Linux/Mac启动脚本
├── 111.html                     # 主应用文件
├── demo_class_data.json         # 演示数据
├── config.json                  # 配置文件
├── import_demo_data.py          # 数据导入脚本
├── demo-mode-simple.js          # 演示模式脚本
├── demo-mode.js                 # 高级演示脚本
├── demo.html                    # 演示页面
├── DEMO_GUIDE.md                # 演示指南
├── CLASS_MANAGEMENT_OPTIMIZATION_SUMMARY.md  # 优化总结
├── FUNCTIONALITY_VERIFICATION_REPORT.md      # 功能验证报告
└── backend/                     # 后端代码
    ├── simple_server.py         # 简易服务器
    ├── main.py                  # 主后端文件
    ├── models.py                # 数据模型
    ├── database.py              # 数据库操作
    ├── judge.py                 # 判题引擎
    ├── schemas.py               # 数据模式
    ├── init_test_data_simple.py # 测试数据
    └── test_api.py              # API测试
```

## 给领导演示的重点

### 1. 专业性展示
- **多班级管理**体现系统完整性
- **可视化图表**展示数据分析能力
- **专业报告**体现系统成熟度

### 2. 实用性展示
- **批量操作**提高工作效率
- **数据导出**方便数据管理
- **比赛管理**支持教学活动

### 3. 技术性展示
- **在线判题**体现技术实力
- **响应式设计**展示前端能力
- **模块化架构**体现工程水平

### 4. 扩展性展示
- **JSON导入**支持数据扩展
- **多语言支持**体现国际化
- **配置灵活**展示可定制性

## 常见问题

### Q: 启动时提示"未检测到Python"？
A: 请安装Python 3.8+，安装时勾选"Add Python to PATH"

### Q: 导入数据后不显示？
A: 刷新页面或重新打开111.html

### Q: 如何重置所有数据？
A: 清除浏览器缓存或使用隐私模式

### Q: 支持多少学生数据？
A: 理论上无限制，建议单班级不超过1000人

### Q: 数据安全吗？
A: 数据存储在浏览器LocalStorage中，本地运行无网络传输

## 技术支持

- **开发部门**: 计算机学院
- **用途**: 教学演示与评估
- **版本**: v1.0.0
- **打包时间**: 2025-03-26

## 开始演示

现在您可以:
1. 双击启动脚本开始系统
2. 按照演示指南操作
3. 向领导展示完整功能
4. 导出数据证明实用性

**祝您演示成功！**
"""
    
    readme_file = package_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   [OK] README.md (详细说明文档)")
    print()
    
    # 6. 创建压缩包
    print("[打包] 创建压缩包...")
    zip_filename = f"{package_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir.parent)
                zipf.write(file_path, arcname)
    
    # 7. 统计信息
    total_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
    total_files = sum(1 for _ in package_dir.rglob('*') if _.is_file())
    
    print("[统计] 打包完成统计:")
    print(f"   打包目录: {package_dir}")
    print(f"   压缩文件: {zip_filename}")
    print(f"   文件数量: {total_files} 个文件")
    print(f"   总大小: {total_size / 1024 / 1024:.2f} MB")
    
    if os.path.exists(zip_filename):
        zip_size = os.path.getsize(zip_filename)
        print(f"   压缩包大小: {zip_size / 1024 / 1024:.2f} MB")
    else:
        print(f"   压缩包大小: 未创建")
    
    print()
    print("[完成] 打包完成！")
    print(f"   便携版已保存到: {zip_filename}")
    print(f"   解压后运行 '启动教学平台.bat' (Windows) 或 './启动教学平台.sh' (Linux/Mac)")
    print()
    print("[演示] 现在可以给领导演示了！")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(create_portable_package())
