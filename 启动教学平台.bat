@echo off
chcp 65001 >nul
echo ========================================
echo        CodeEdu 教学平台启动器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)

echo [信息] 检查依赖包...
cd /d "%~dp0"

REM 检查前端依赖
if not exist "frontend\node_modules\" (
    echo [信息] 安装前端依赖...
    cd frontend
    call npm install
    cd ..
)

REM 启动后端服务器
echo [信息] 启动后端服务器 (端口: 5000)...
start "CodeEdu后端" cmd /k "cd /d "%~dp0backend" && python simple_server.py"

REM 等待后端启动
echo [信息] 等待后端服务器启动...
timeout /t 3 /nobreak >nul

REM 启动前端开发服务器
echo [信息] 启动前端开发服务器 (端口: 5173)...
start "CodeEdu前端" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo [成功] 平台启动完成！
echo.
echo 访问地址:
echo 1. 前端界面: http://localhost:5173
echo 2. 后端API: http://localhost:5000
echo.
echo 测试账号:
echo - 教师: teacher / 123456
echo - 学生: student / 123456
echo ========================================
echo.
echo 按任意键打开浏览器访问前端界面...
pause >nul

start http://localhost:5173
echo.
echo 按任意键退出...
pause >nul
