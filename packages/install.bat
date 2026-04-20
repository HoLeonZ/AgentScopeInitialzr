@echo off
REM ============================================================
REM AgentScope Initializr - 离线安装脚本
REM 将 packages 文件夹拷贝到目标电脑后，运行此脚本
REM ============================================================

echo ============================================================
echo AgentScope Initializr - 离线安装
echo ============================================================
echo.

REM 检查是否在 packages 目录
if not exist requirements.txt (
    echo 错误: 请在 packages 目录下运行此脚本
    echo.
    echo 用法:
    echo   cd packages
    echo   install.bat
    goto :end
)

echo 正在安装依赖包...
echo.

REM 安装所有依赖
pip install --no-index --find-links=. -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo 安装成功！
    echo ============================================================
    echo.
    echo 注意: 如果使用了 playwright，请运行以下命令安装浏览器:
    echo   playwright install chromium
    echo.
) else (
    echo.
    echo 警告: 安装过程中出现错误
    echo 请检查 Python 环境是否正确配置
)

:end
pause
