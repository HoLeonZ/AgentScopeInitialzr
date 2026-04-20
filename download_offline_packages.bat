@echo off
REM ============================================================
REM AgentScope Initializr - Windows x86_64 离线包下载脚本
REM 在 Windows x86_64 联网机器上运行此脚本
REM 下载所有包到 packages 目录，然后拷贝到离线机器
REM ============================================================

setlocal

set "TARGET_DIR=packages"
set "PYTHON_CMD=python"

echo ============================================================
echo AgentScope Initializr - 离线依赖包下载
echo ============================================================
echo.
echo 目标目录: %TARGET_DIR%
echo 平台: Windows x86_64
echo.

REM 检查 Python
%PYTHON_CMD% --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.11+
    goto :end
)

REM 创建目标目录
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

REM 进入目标目录
cd /d "%~dp0%TARGET_DIR%"
set "DOWNLOAD_DIR=%CD%"
cd /d "%~dp0"

echo 下载目录: %DOWNLOAD_DIR%
echo.

echo [1/4] 下载 Python wheel 包...
echo ------------------------------------------------

REM 核心依赖
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" agentscope>=0.1.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" python-dotenv>=1.0.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" click>=8.1.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" jinja2>=3.1.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" pydantic>=2.0.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" aiofiles>=23.0.0

REM Web 服务
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" fastapi>=0.100.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" uvicorn>=0.23.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" python-multipart>=0.0.6
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" h11>=0.14.0

REM 模型提供商
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" openai>=1.0.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" anthropic>=0.18.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" dashscope>=1.0.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" google-generativeai>=0.3.0

REM 记忆存储
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" redis>=5.0.0

REM Agent 类型
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" httpx>=0.27.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" playwright>=1.40.0

REM 知识库
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" qdrant-client>=1.7.0

REM 工具
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" tavily-python>=0.3.0

echo.
echo [2/4] 下载 RAGAS 评测相关包...
echo ------------------------------------------------
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" ragas>=0.1.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" langchain>=0.1.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" langchain-openai>=0.0.5
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" pandas>=2.0.0
%PYTHON_CMD% -m pip download --no-deps --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" datasets>=2.14.0

echo.
echo [3/4] 下载传递依赖...
echo ------------------------------------------------
REM 使用 pipdeptree 分析并下载所有传递依赖
%PYTHON_CMD% -m pip download --platform win_amd64 --python-version 311 --implementation cp --dest "%DOWNLOAD_DIR%" -r requirements_offline.txt

echo.
echo [4/4] 创建安装说明...
echo ------------------------------------------------

REM 复制 requirements 文件
copy requirements_offline.txt "%DOWNLOAD_DIR%\requirements.txt" >nul 2>&1

REM 创建安装脚本
(
echo @echo off
echo echo ============================================================
echo echo AgentScope Initializr - 离线安装
echo echo ============================================================
echo echo.
echo echo 正在从本地 packages 目录安装依赖...
echo.
echo pip install --no-index --find-links=. -r requirements.txt
echo.
echo 安装完成！
echo.
echo 注意: 如果安装失败，可能需要安装 Microsoft Visual C++ Redistributable
echo 下载地址: https://aka.ms/vs/17/release/vc_redist.x64.exe
) > "%DOWNLOAD_DIR%\install.bat"

echo.
echo ============================================================
echo 下载完成！
echo ============================================================
echo.
echo 下载目录: %~dp0%TARGET_DIR%
echo.
echo 请将此目录拷贝到离线 Windows 机器上，然后运行:
echo   cd packages
echo   install.bat
echo.
echo 或直接运行:
echo   pip install --no-index --find-links=. -r requirements.txt
echo.

:end
endlocal
pause
