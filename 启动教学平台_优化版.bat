@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    CodeEdu 教学平台 - 国内优化版
echo ========================================
echo.
echo 本版本针对国内网络环境优化，支持离线部署
echo.

REM 设置窗口标题
title CodeEdu 教学平台 - 国内优化版

REM 检查Python是否安装
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    echo.
    echo 解决方案：
    echo 1. 从 https://www.python.org/downloads/ 下载Python 3.8+
    echo 2. 安装时勾选"Add Python to PATH"
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

REM 显示Python版本
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo    %python_version%

REM 检查Node.js是否安装（可选）
echo [2/5] 检查Node.js环境（可选）...
node --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未找到Node.js，前端开发服务器将无法启动
    echo    但可以使用预编译的前端文件
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do set node_version=%%i
    echo    %node_version%
)

REM 配置国内镜像源
echo [3/5] 配置国内镜像源...
echo.

REM 配置pip镜像源
if not exist "%APPDATA%\pip" mkdir "%APPDATA%\pip"
echo [global] > "%APPDATA%\pip\pip.ini"
echo index-url = https://pypi.tuna.tsinghua.edu.cn/simple >> "%APPDATA%\pip\pip.ini"
echo trusted-host = pypi.tuna.tsinghua.edu.cn >> "%APPDATA%\pip\pip.ini"
echo timeout = 6000 >> "%APPDATA%\pip\pip.ini"
echo    pip镜像源已配置为清华源

REM 检查Python依赖
echo [4/5] 检查Python依赖...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo    正在安装Python依赖（使用国内镜像）...
    pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --timeout 6000
    if errorlevel 1 (
        echo [错误] Python依赖安装失败
        echo.
        echo 解决方案：
        echo 1. 检查网络连接
        echo 2. 手动运行：pip install -r requirements.txt
        echo 3. 或使用离线安装包
        echo.
        pause
        exit /b 1
    )
    echo    Python依赖安装完成
) else (
    echo    Python依赖已安装
)

REM 检查前端依赖
echo [5/5] 检查前端依赖...
if exist "frontend\node_modules" (
    echo    前端依赖已存在
) else (
    if exist "frontend\package.json" (
        echo    正在安装前端依赖（使用国内镜像）...
        cd frontend
        call npm install --registry=https://registry.npmmirror.com/
        if errorlevel 1 (
            echo [警告] 前端依赖安装失败，但后端仍可运行
            echo    可以手动运行：cd frontend && npm install
        ) else (
            echo    前端依赖安装完成
        )
        cd ..
    ) else (
        echo [警告] 未找到前端项目文件
    )
)

echo.
echo ========================================
echo    环境检查完成，正在启动服务...
echo ========================================
echo.

REM 启动后端服务器
echo [启动] 后端服务器 (http://localhost:5000)
start "CodeEdu后端" cmd /k "python backend/simple_server.py"

REM 等待后端启动
echo    等待后端启动...（3秒）
timeout /t 3 /nobreak >nul

REM 检查后端是否启动成功
curl --silent --output nul --fail http://localhost:5000
if errorlevel 1 (
    echo [警告] 后端启动可能失败，请检查端口5000是否被占用
    echo    可以手动修改backend/simple_server.py中的端口号
)

REM 启动前端开发服务器
if exist "frontend\node_modules" (
    echo [启动] 前端开发服务器 (http://localhost:5173)
    start "CodeEdu前端" cmd /k "cd frontend && npm run dev"
    
    REM 等待前端启动
    echo    等待前端启动...（5秒）
    timeout /t 5 /nobreak >nul
) else (
    echo [信息] 前端依赖未安装，跳过前端启动
    echo    如需启动前端，请先运行：cd frontend && npm install
)

echo.
echo ========================================
echo        CodeEdu 教学平台已启动
echo ========================================
echo.
echo 访问地址：
echo 1. 前端界面：http://localhost:5173
echo 2. 后端API：http://localhost:5000
echo 3. API文档：http://localhost:5000
echo.
echo 测试账户：
echo - 学生：student1 / 123456
echo - 教师：teacher2 / 123456
echo - 管理员：admin2 / 123456
echo.
echo 数据管理工具：
echo - 图形界面：运行"启动数据导入工具.bat"
echo - 命令行：python data_import_tool_enhanced.py help
echo.
echo 按任意键打开浏览器访问前端界面...
pause >nul

REM 尝试打开浏览器
start "" "http://localhost:5173"

echo.
echo 服务正在运行，按Ctrl+C停止服务
echo 注意：关闭此窗口将停止所有服务
echo.
pause
