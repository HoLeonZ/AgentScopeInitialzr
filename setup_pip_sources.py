#!/usr/bin/env python3
"""
Pip 源自动配置脚本
自动检测操作系统并配置 pip 源（支持 Windows、Linux、macOS）
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# pip 源配置
PIP_SOURCES = {
    "primary": "https://mirrors.aliyun.com/pypi/simple/",
    "mirrors": [
        "https://mirrors.aliyun.com/pypi/simple/",
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://mirrors.cloud.tencent.com/pypi/simple",
        "https://repo.huaweicloud.com/repository/pypi/simple",
        "https://pypi.doubanio.com/simple",
        "https://pypi.org/simple",
    ]
}

# 信任的主机
TRUSTED_HOSTS = [
    "mirrors.aliyun.com",
    "pypi.tuna.tsinghua.edu.cn",
    "mirrors.cloud.tencent.com",
    "repo.huaweicloud.com",
    "pypi.doubanio.com",
    "pypi.org",
]


def get_pip_config_dir() -> Path:
    """获取 pip 配置目录"""
    if platform.system() == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "pip"
    else:
        return Path.home() / ".pip"


def get_pip_config_file() -> Path:
    """获取 pip 配置文件路径"""
    if platform.system() == "Windows":
        return get_pip_config_dir() / "pip.ini"
    else:
        return get_pip_config_dir() / "pip.conf"


def get_pip_global_location() -> Path:
    """获取全局 pip 配置位置（需要管理员权限）"""
    if platform.system() == "Windows":
        python_path = Path(sys.executable).parent
        return python_path / "pip.ini"
    else:
        return Path("/etc/pip.conf")


def create_pip_config() -> Path:
    """创建 pip 配置文件"""
    config_dir = get_pip_config_dir()
    config_file = get_pip_config_file()

    # 创建配置目录
    config_dir.mkdir(parents=True, exist_ok=True)

    # 构建配置文件内容
    trusted_hosts_str = "\n".join(f"    {host}" for host in TRUSTED_HOSTS)

    content = f'''[global]
timeout = 120
index-url = {PIP_SOURCES["primary"]}
trusted-host = {trusted_hosts_str}

[install]
index-url = {PIP_SOURCES["primary"]}
extra-index-url =
'''

    # 添加备用源
    extra_urls = "\n".join(f"    {url}" for url in PIP_SOURCES["mirrors"][1:])
    content += extra_urls

    # 写入配置文件
    config_file.write_text(content, encoding="utf-8")

    return config_file


def create_pip_windows_reg():
    """创建 Windows 注册表配置（全局生效）"""
    if platform.system() != "Windows":
        return None

    try:
        import winreg
    except ImportError:
        return None

    try:
        # 创建或打开 pip 配置键
        key_path = r"Software\Python\PythonCore\{}\InstallPath".format(
            sys.version_info.major
        )
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)

        # 创建 pip.ini 文件
        pip_ini_path = Path(sys.executable).parent / "pip.ini"
        create_pip_config()

        return pip_ini_path
    except Exception:
        return None


def setup_pip_sources():
    """设置 pip 源"""
    print("=" * 60)
    print("Pip 源自动配置工具")
    print("=" * 60)
    print()

    system = platform.system()
    print(f"检测到操作系统: {system}")
    print(f"Python 版本: {platform.python_version()}")
    print()

    # 尝试创建用户级配置
    try:
        config_file = create_pip_config()
        print(f"✓ 已创建用户级配置: {config_file}")
        print(f"  主源: {PIP_SOURCES['primary']}")
        print(f"  备用源数量: {len(PIP_SOURCES['mirrors']) - 1}")
    except Exception as e:
        print(f"✗ 用户级配置失败: {e}")
        config_file = None

    print()

    # 测试 pip 配置
    print("测试 pip 配置...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "config", "list"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ pip 配置成功")
        else:
            print("⚠ pip config 命令不可用，使用环境变量方式")
    except Exception:
        pass

    print()
    print("=" * 60)
    print("配置完成！")
    print("=" * 60)
    print()
    print("使用方式:")
    print("  1. 直接安装离线包:")
    print("     pip install --no-index --find-links=./packages -r requirements.txt")
    print()
    print("  2. 联网安装依赖:")
    print("     pip install -r requirements.txt")
    print()
    print("  3. 下载离线包:")
    print("     pip download -r requirements.txt --no-deps -d ./packages")
    print()
    print(f"  主源: {PIP_SOURCES['primary']}")
    print()

    return config_file


def download_packages(packages_file: str = "requirements.txt", target_dir: str = "packages"):
    """下载离线包"""
    print("=" * 60)
    print("离线包下载工具")
    print("=" * 60)
    print()

    target_path = Path(target_dir)
    target_path.mkdir(exist_ok=True)

    print(f"目标目录: {target_path.absolute()}")
    print(f"平台: Windows x86_64")
    print(f"Python: {platform.python_version()}")
    print()

    # 读取依赖文件
    req_file = Path(packages_file)
    if not req_file.exists():
        print(f"错误: 找不到 {packages_file}")
        return False

    with open(req_file, "r", encoding="utf-8") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"需要下载的包数量: {len(packages)}")
    print()

    # 下载命令
    cmd = [
        sys.executable, "-m", "pip", "download",
        "--no-deps",
        "--platform", "win_amd64",
        "--python-version", "311",
        "--implementation", "cp",
        "--only-binary", ":all:",
        "-d", str(target_path),
        "-r", str(req_file),
    ]

    print("开始下载...")
    print(f"命令: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, text=True)

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print()
            print("=" * 60)
            print("下载完成！")
            print("=" * 60)

            # 统计
            files = list(target_path.glob("*.whl"))
            total_size = sum(f.stat().st_size for f in files)
            print(f"文件数量: {len(files)}")
            print(f"总大小: {total_size / 1024 / 1024:.2f} MB")

            return True
        else:
            print(f"下载失败，退出码: {result.returncode}")
            return False

    except Exception as e:
        print(f"错误: {e}")
        return False


def install_offline(target_dir: str = "packages", requirements_file: str = "requirements.txt"):
    """离线安装"""
    print("=" * 60)
    print("离线包安装工具")
    print("=" * 60)
    print()

    target_path = Path(target_dir)
    req_file = Path(requirements_file)

    if not target_path.exists():
        print(f"错误: 找不到目录 {target_dir}")
        return False

    if not req_file.exists():
        # 尝试在 packages 目录中查找
        req_in_packages = target_path / "requirements.txt"
        if req_in_packages.exists():
            req_file = req_in_packages
            print(f"找到 requirements.txt: {req_file}")

    if not req_file.exists():
        print(f"错误: 找不到 {requirements_file}")
        return False

    print(f"安装目录: {target_path.absolute()}")
    print(f"依赖文件: {req_file}")
    print()

    # 安装命令
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--no-index",
        "--find-links", str(target_path),
        "-r", str(req_file),
    ]

    print("开始安装...")
    print(f"命令: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, text=True)

        if result.stdout:
            # 只显示最后 50 行
            lines = result.stdout.strip().split("\n")
            if len(lines) > 50:
                print("...\n" + "\n".join(lines[-50:]))
            else:
                print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print()
            print("=" * 60)
            print("安装完成！")
            print("=" * 60)
            return True
        else:
            print(f"安装失败，退出码: {result.returncode}")
            return False

    except Exception as e:
        print(f"错误: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pip 源配置和离线包管理工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # setup 命令
    subparsers.add_parser("setup", help="配置 pip 源")

    # download 命令
    download_parser = subparsers.add_parser("download", help="下载离线包")
    download_parser.add_argument("-r", "--requirements", default="requirements.txt", help="依赖文件")
    download_parser.add_argument("-d", "--dir", default="packages", help="目标目录")

    # install 命令
    install_parser = subparsers.add_parser("install", help="离线安装")
    install_parser.add_argument("-d", "--dir", default="packages", help="包目录")
    install_parser.add_argument("-r", "--requirements", default="requirements.txt", help="依赖文件")

    args = parser.parse_args()

    if args.command == "setup" or args.command is None:
        setup_pip_sources()
    elif args.command == "download":
        download_packages(args.requirements, args.dir)
    elif args.command == "install":
        install_offline(args.dir, args.requirements)
