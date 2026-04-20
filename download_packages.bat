@echo off
REM AgentScope Initializr - Windows x86_64 包下载脚本
REM 在 Windows CMD 或 PowerShell 中运行此脚本预下载所有依赖包

setlocal enabledelayedexpansion

set "TARGET_DIR=packages"
set "PYTHON_CMD=python"

echo ========================================================
echo AgentScope Initializr - 依赖包下载
echo ========================================================
echo.
echo 目标目录: %TARGET_DIR%
echo 平台: Windows x86_64
echo.

REM 创建目标目录
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

REM 创建临时 requirements 文件
set "TEMP_REQ=%TARGET_DIR%\temp_requirements.txt"

echo agentscope>=0.1.0 > "%TEMP_REQ%"
echo python-dotenv>=1.0.0 >> "%TEMP_REQ%"
echo openai>=1.0.0 >> "%TEMP_REQ%"
echo anthropic>=0.18.0 >> "%TEMP_REQ%"
echo dashscope>=1.0.0 >> "%TEMP_REQ%"
echo google-generativeai>=0.3.0 >> "%TEMP_REQ%"
echo mem0ai>=0.1.0 >> "%TEMP_REQ%"
echo redis>=5.0.0 >> "%TEMP_REQ%"
echo zep>=1.0.0 >> "%TEMP_REQ%"
echo oceanbase>=1.0.0 >> "%TEMP_REQ%"
echo httpx>=0.27.0 >> "%TEMP_REQ%"
echo playwright>=1.40.0 >> "%TEMP_REQ%"
echo qdrant-client>=1.7.0 >> "%TEMP_REQ%"
echo ragas>=0.1.0 >> "%TEMP_REQ%"
echo langchain>=0.1.0 >> "%TEMP_REQ%"
echo langchain-openai>=0.0.5 >> "%TEMP_REQ%"
echo pandas>=2.0.0 >> "%TEMP_REQ%"
echo datasets>=2.14.0 >> "%TEMP_REQ%"
echo aiofiles>=23.0.0 >> "%TEMP_REQ%"
echo fastapi>=0.100.0 >> "%TEMP_REQ%"
echo uvicorn>=0.23.0 >> "%TEMP_REQ%"
echo click>=8.1.0 >> "%TEMP_REQ%"
echo jinja2>=3.1.0 >> "%TEMP_REQ%"
echo pydantic>=2.0.0 >> "%TEMP_REQ%"
echo tavily-python>=0.3.0 >> "%TEMP_REQ%"
echo python-multipart>=0.0.6 >> "%TEMP_REQ%"

echo 开始下载依赖包...
echo.

REM 下载包（优先下载 wheel，如果不存在则下载源码）
%PYTHON_CMD% -m pip download ^
    --only-binary=:all: ^
    --platform win_amd64 ^
    --python-version 311 ^
    --implementation cp ^
    --dest "%TARGET_DIR%" ^
    -r "%TEMP_REQ%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 部分包没有 Windows wheel，开始下载源码包...
    %PYTHON_CMD% -m pip download ^
        --no-deps ^
        --dest "%TARGET_DIR%" ^
        -r "%TEMP_REQ%"
)

REM 删除临时文件
del "%TEMP_REQ%"

REM 创建正式的 requirements.txt
copy "%TARGET_DIR%\requirements.txt" "%TARGET_DIR%\requirements_backup.txt" 2>nul
echo agentscope>=0.1.0 > "%TARGET_DIR%\requirements.txt"
echo python-dotenv>=1.0.0 >> "%TARGET_DIR%\requirements.txt"
echo openai>=1.0.0 >> "%TARGET_DIR%\requirements.txt"
echo anthropic>=0.18.0 >> "%TARGET_DIR%\requirements.txt"
echo dashscope>=1.0.0 >> "%TARGET_DIR%\requirements.txt"
echo google-generativeai>=0.3.0 >> "%TARGET_DIR%\requirements.txt"
echo mem0ai>=0.1.0 >> "%TARGET_DIR%\requirements.txt"
echo redis>=5.0.0 >> "%TARGET_DIR%\requirements.txt"
echo zep>=1.0.0 >> "%TARGET_DIR%\requirements.txt"
echo oceanbase>=1.0.0 >> "%TARGET_DIR%\requirements.txt"
echo httpx>=0.27.0 >> "%TARGET_DIR%\requirements.txt"
echo playwright>=1.40.0 >> "%TARGET_DIR%\requirements.txt"
echo qdrant-client>=1.7.0 >> "%TARGET_DIR%\requirements.txt"
echo ragas>=0.1.0 >> "%TARGET_DIR%\requirements.txt"
echo langchain>=0.1.0 >> "%TARGET_DIR%\requirements.txt"
echo langchain-openai>=0.0.5 >> "%TARGET_DIR%\requirements.txt"
echo pandas>=2.0.0 >> "%TARGET_DIR%\requirements.txt"
echo datasets>=2.14.0 >> "%TARGET_DIR%\requirements.txt"
echo aiofiles>=23.0.0 >> "%TARGET_DIR%\requirements.txt"
echo fastapi>=0.100.0 >> "%TARGET_DIR%\requirements.txt"
echo uvicorn>=0.23.0 >> "%TARGET_DIR%\requirements.txt"
echo click>=8.1.0 >> "%TARGET_DIR%\requirements.txt"
echo jinja2>=3.1.0 >> "%TARGET_DIR%\requirements.txt"
echo pydantic>=2.0.0 >> "%TARGET_DIR%\requirements.txt"
echo tavily-python>=0.3.0 >> "%TARGET_DIR%\requirements.txt"
echo python-multipart>=0.0.6 >> "%TARGET_DIR%\requirements.txt"

echo.
echo ========================================================
echo 下载完成！
echo ========================================================
echo.
echo 下载的文件位于: %CD%\%TARGET_DIR%
echo.
echo 安装方法:
echo   pip install --no-index --find-links=%TARGET_DIR% -r %TARGET_DIR%\requirements.txt
echo.
echo 提示: 首次使用 playwright 时需要运行:
echo   playwright install chromium
echo.

endlocal
