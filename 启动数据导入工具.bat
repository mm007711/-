@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    CodeEdu 数据导入工具启动器
echo ========================================
echo.
echo 正在启动图形界面数据导入工具...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    echo 可以从 https://www.python.org/downloads/ 下载
    pause
    exit /b 1
)

REM 检查数据库文件是否存在
if not exist "codeedu.db" (
    echo [警告] 未找到数据库文件 codeedu.db
    echo 请确保CodeEdu系统已正确安装
    echo.
)

REM 启动GUI工具
echo 正在启动数据导入工具...
python data_import_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 启动失败，请检查以下可能的问题：
    echo 1. 缺少必要的Python库：pip install pandas openpyxl
    echo 2. 数据库文件路径不正确
    echo 3. Python版本不兼容
    echo.
    pause
    exit /b 1
)

echo.
echo 数据导入工具已关闭。
pause
