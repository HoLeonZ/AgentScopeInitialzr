@echo off
REM ============================================================
REM AgentScope Initializr - Windows 离线包管理工具
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PACKAGES_DIR=%SCRIPT_DIR%"
set "REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt"

echo ============================================================
echo AgentScope Initializr - 离线包管理
echo ============================================================
echo.
echo 1. 配置 pip 源（国内加速）
echo 2. 下载离线包
echo 3. 离线安装
echo 4. 一键安装（配置源 + 离线安装）
echo 5. 退出
echo.

set /p choice=请选择操作 (1-5):

if "%choice%"=="1" goto :setup_pip
if "%choice%"=="2" goto :download
if "%choice%"=="3" goto :install_offline
if "%choice%"=="4" goto :full_install
if "%choice%"=="5" goto :end

echo 无效选择，请重新运行
goto :end

:setup_pip
echo.
echo ============================================================
echo 配置 pip 源
echo ============================================================
echo.

REM 创建 pip 配置目录
set "PIP_DIR=%APPDATA%\pip"
if not exist "%PIP_DIR%" mkdir "%PIP_DIR%"

REM 创建 pip.ini
echo [global] > "%PIP_DIR%\pip.ini"
echo timeout = 120 >> "%PIP_DIR%\pip.ini"
echo index-url = https://mirrors.aliyun.com/pypi/simple/ >> "%PIP_DIR%\pip.ini"
echo trusted-host = mirrors.aliyun.com >> "%PIP_DIR%\pip.ini"
echo. >> "%PIP_DIR%\pip.ini"
echo [install] >> "%PIP_DIR%\pip.ini"
echo index-url = https://mirrors.aliyun.com/pypi/simple/ >> "%PIP_DIR%\pip.ini"
echo extra-index-url = https://pypi.tuna.tsinghua.edu.cn/simple >> "%PIP_DIR%\pip.ini"
echo                      https://mirrors.cloud.tencent.com/pypi/simple >> "%PIP_DIR%\pip.ini"
echo                      https://repo.huaweicloud.com/repository/pypi/simple >> "%PIP_DIR%\pip.ini"
echo                      https://pypi.doubanio.com/simple >> "%PIP_DIR%\pip.ini"
echo                      https://pypi.org/simple >> "%PIP_DIR%\pip.ini"

echo.
echo ✓ pip 源配置完成！
echo   配置文件: %PIP_DIR%\pip.ini
echo   主源: 阿里云
echo   备用源: 清华、腾讯云、华为云、豆瓣、PyPI官方
echo.
echo 测试 pip 配置...
python -m pip config list

goto :end

:download
echo.
echo ============================================================
echo 下载离线包
echo ============================================================
echo.

set /p version=请输入 Python 版本 (311 默认):
if "!version!"=="" set "version=311"

echo.
echo 正在下载离线包到 packages 目录...
echo.

python -m pip download ^
    --no-deps ^
    --platform win_amd64 ^
    --python-version !version! ^
    --implementation cp ^
    --only-binary :all: ^
    --dest "%PACKAGES_DIR%" ^
    -r "%REQUIREMENTS_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo 下载完成！
    echo ============================================================
    echo.
    echo 请查看 %PACKAGES_DIR% 目录中的 .whl 文件
) else (
    echo.
    echo 下载过程中出现错误
)

goto :end

:install_offline
echo.
echo ============================================================
echo 离线安装
echo ============================================================
echo.

if not exist "%PACKAGES_DIR%" (
    echo 错误: packages 目录不存在
    goto :end
)

if not exist "%REQUIREMENTS_FILE%" (
    set "REQUIREMENTS_FILE=%PACKAGES_DIR%\requirements.txt"
)

echo 正在安装依赖包...
echo.

pip install --no-index --find-links="%PACKAGES_DIR%" -r "%REQUIREMENTS_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo 安装完成！
    echo ============================================================
    echo.
    echo 注意: 如果使用了 playwright，请运行以下命令安装浏览器:
    echo   playwright install chromium
) else (
    echo.
    echo 安装过程中出现错误
)

goto :end

:full_install
echo.
echo ============================================================
echo 一键安装（配置源 + 离线安装）
echo ============================================================
echo.

echo Step 1: 配置 pip 源
echo ----------------------
call :setup_pip

echo.
echo Step 2: 离线安装
echo ----------------------
call :install_offline

goto :end

:end
echo.
pause
endlocal
