@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   CodeEdu 离线部署包创建工具
echo ========================================
echo.
echo 此工具将创建完整的离线部署包，包含：
echo 1. 所有Python依赖包
echo 2. 所有Node.js依赖包
echo 3. 预置数据库和配置文件
echo 4. 一键启动脚本
echo.

REM 设置窗口标题
title CodeEdu 离线部署包创建工具

REM 检查Python是否安装
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

REM 检查Node.js是否安装
echo [2/6] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未找到Node.js，将跳过前端依赖打包
    set skip_frontend=1
) else (
    set skip_frontend=0
)

REM 创建输出目录
echo [3/6] 创建输出目录...
set output_dir=CodeEdu_离线部署包_%date:~0,4%%date:~5,2%%date:~8,2%
if exist "%output_dir%" (
    echo    目录已存在，删除旧版本...
    rmdir /s /q "%output_dir%"
)
mkdir "%output_dir%"
mkdir "%output_dir%\backend"
mkdir "%output_dir%\frontend"
mkdir "%output_dir%\tools"
mkdir "%output_dir%\data"
echo    输出目录：%output_dir%

REM 复制项目文件
echo [4/6] 复制项目文件...
xcopy backend "%output_dir%\backend" /E /I /Y
xcopy frontend "%output_dir%\frontend" /E /I /Y
xcopy *.py "%output_dir%\tools" /Y
xcopy *.bat "%output_dir%" /Y
xcopy *.md "%output_dir%" /Y
xcopy *.txt "%output_dir%" /Y
xcopy *.json "%output_dir%" /Y
xcopy *.csv "%output_dir%\data" /Y
copy codeedu.db "%output_dir%\" >nul 2>&1
echo    项目文件复制完成

REM 下载Python依赖包
echo [5/6] 下载Python依赖包...
cd "%output_dir%"
if exist "python_packages" rmdir /s /q "python_packages"
mkdir python_packages
pip download -r requirements.txt -d python_packages --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --timeout 6000
if errorlevel 1 (
    echo [警告] Python依赖包下载失败
) else (
    echo    Python依赖包下载完成
)

REM 创建离线安装脚本
echo    创建Python离线安装脚本...
echo @echo off > install_python_deps.bat
echo echo 正在安装Python依赖包... >> install_python_deps.bat
echo pip install --no-index --find-links=python_packages -r requirements.txt >> install_python_deps.bat
echo if errorlevel 1 ( >> install_python_deps.bat
echo     echo [错误] 依赖安装失败 >> install_python_deps.bat
echo     pause >> install_python_deps.bat
echo     exit /b 1 >> install_python_deps.bat
echo ) >> install_python_deps.bat
echo echo Python依赖安装完成 >> install_python_deps.bat
echo pause >> install_python_deps.bat

REM 处理前端依赖
if "%skip_frontend%"=="0" (
    echo [6/6] 打包前端依赖...
    cd frontend
    if exist node_modules (
        echo    打包node_modules...
        tar -czf ..\node_modules.tar.gz node_modules/
        if errorlevel 1 (
            echo [警告] node_modules打包失败，尝试使用7zip...
            7z a -ttar ..\node_modules.tar node_modules\ >nul 2>&1
            if errorlevel 1 (
                echo [警告] 7zip打包也失败，跳过前端依赖打包
            ) else (
                7z a -tgzip ..\node_modules.tar.gz ..\node_modules.tar >nul 2>&1
                del ..\node_modules.tar
                echo    node_modules打包完成
            )
        ) else (
            echo    node_modules打包完成
        )
    ) else (
        echo [信息] 未找到node_modules，将跳过前端依赖打包
    )
    
    REM 创建前端离线安装脚本
    echo    创建前端离线安装脚本...
    cd ..
    echo @echo off > install_frontend_deps.bat
    echo echo 正在安装前端依赖包... >> install_frontend_deps.bat
    echo cd frontend >> install_frontend_deps.bat
    echo if exist node_modules.tar.gz ( >> install_frontend_deps.bat
    echo     echo 解压node_modules... >> install_frontend_deps.bat
    echo     tar -xzf node_modules.tar.gz >> install_frontend_deps.bat
    echo     if errorlevel 1 ( >> install_frontend_deps.bat
    echo         echo [错误] 解压失败，尝试使用7zip... >> install_frontend_deps.bat
    echo         7z x node_modules.tar.gz -y >nul 2>&1 >> install_frontend_deps.bat
    echo         if errorlevel 1 ( >> install_frontend_deps.bat
    echo             echo [错误] 7zip解压也失败 >> install_frontend_deps.bat
    echo         ) >> install_frontend_deps.bat
    echo     ) >> install_frontend_deps.bat
    echo     echo 重建依赖链接... >> install_frontend_deps.bat
    echo     npm rebuild >> install_frontend_deps.bat
    echo ) else ( >> install_frontend_deps.bat
    echo     echo [信息] 未找到node_modules.tar.gz，将在线安装依赖 >> install_frontend_deps.bat
    echo     npm install --registry=https://registry.npmmirror.com/ >> install_frontend_deps.bat
    echo ) >> install_frontend_deps.bat
    echo echo 前端依赖安装完成 >> install_frontend_deps.bat
    echo pause >> install_frontend_deps.bat
    cd ..
) else (
    echo [6/6] 跳过前端依赖打包（Node.js未安装）
)

REM 创建一键安装脚本
echo    创建一键安装脚本...
cd "%output_dir%"
echo @echo off > 一键安装.bat
echo chcp 65001 ^>nul >> 一键安装.bat
echo echo. >> 一键安装.bat
echo echo ======================================== >> 一键安装.bat
echo echo    CodeEdu 离线安装工具 >> 一键安装.bat
echo echo ======================================== >> 一键安装.bat
echo echo. >> 一键安装.bat
echo echo 正在安装所有依赖... >> 一键安装.bat
echo echo. >> 一键安装.bat
echo call install_python_deps.bat >> 一键安装.bat
echo if exist install_frontend_deps.bat ( >> 一键安装.bat
echo     call install_frontend_deps.bat >> 一键安装.bat
echo ) >> 一键安装.bat
echo echo. >> 一键安装.bat
echo echo ======================================== >> 一键安装.bat
echo echo    安装完成！ >> 一键安装.bat
echo echo ======================================== >> 一键安装.bat
echo echo. >> 一键安装.bat
echo echo 现在可以运行以下命令启动系统： >> 一键安装.bat
echo echo 1. 启动教学平台_优化版.bat - 完整开发环境 >> 一键安装.bat
echo echo 2. 启动数据导入工具.bat - 数据管理工具 >> 一键安装.bat
echo echo. >> 一键安装.bat
echo pause >> 一键安装.bat

REM 创建使用说明
echo    创建使用说明文档...
echo # CodeEdu 离线部署包使用说明 > 使用说明.txt
echo. >> 使用说明.txt
echo ## 系统要求 >> 使用说明.txt
echo 1. Windows 7/8/10/11 操作系统 >> 使用说明.txt
echo 2. Python 3.8+（已包含在安装脚本中） >> 使用说明.txt
echo 3. Node.js 16+（可选，用于前端开发） >> 使用说明.txt
echo. >> 使用说明.txt
echo ## 安装步骤 >> 使用说明.txt
echo 1. 解压本压缩包到任意目录 >> 使用说明.txt
echo 2. 双击运行"一键安装.bat"安装所有依赖 >> 使用说明.txt
echo 3. 双击运行"启动教学平台_优化版.bat"启动系统 >> 使用说明.txt
echo. >> 使用说明.txt
echo ## 访问地址 >> 使用说明.txt
echo - 前端界面：http://localhost:5173 >> 使用说明.txt
echo - 后端API：http://localhost:5000 >> 使用说明.txt
echo. >> 使用说明.txt
echo ## 测试账户 >> 使用说明.txt
echo - 学生：student1 / 123456 >> 使用说明.txt
echo - 教师：teacher2 / 123456 >> 使用说明.txt
echo - 管理员：admin2 / 123456 >> 使用说明.txt
echo. >> 使用说明.txt
echo ## 数据管理 >> 使用说明.txt
echo 运行"启动数据导入工具.bat"使用图形界面管理数据 >> 使用说明.txt
echo. >> 使用说明.txt
echo ## 注意事项 >> 使用说明.txt
echo 1. 确保端口5000和5173未被占用 >> 使用说明.txt
echo 2. 首次运行可能需要几分钟安装依赖 >> 使用说明.txt
echo 3. 关闭防火墙或添加例外规则以允许局域网访问 >> 使用说明.txt

cd ..

echo.
echo ========================================
echo     离线部署包创建完成！
echo ========================================
echo.
echo 输出目录：%output_dir%
echo.
echo 包含内容：
echo 1. 完整的项目代码
echo 2. Python依赖包（离线安装）
if "%skip_frontend%"=="0" (
    echo 3. Node.js依赖包（离线安装）
) else (
    echo 3. [跳过] Node.js依赖包
)
echo 4. 预置数据库和配置文件
echo 5. 一键安装脚本
echo 6. 详细使用说明
echo.
echo 下一步：
echo 1. 将"%output_dir%"目录压缩为ZIP文件
echo 2. 分发到目标机器
echo 3. 解压后运行"一键安装.bat"
echo 4. 运行"启动教学平台_优化版.bat"
echo.
echo 按任意键打开输出目录...
pause >nul

REM 打开输出目录
explorer "%output_dir%"

echo.
echo 完成！
pause
