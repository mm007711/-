@echo off
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
start /B python backend\simple_server.py

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
