# 🚀 AgentScope Initializr - ARM64 优雅部署方案

一套完整的、优雅的 ARM64 部署解决方案，包含自动化部署脚本、监控工具和管理界面。

## ✨ 特性

- 🎨 **优雅的界面** - 彩色终端输出，清晰的状态指示
- 🤖 **完全自动化** - 一键部署，无需手动配置
- 📊 **健康监控** - 实时服务状态检查和性能分析
- 🛠️ **便捷管理** - 简单命令即可管理服务
- 🔒 **生产就绪** - 包含系统服务和资源限制配置

## 📦 文件清单

| 文件 | 描述 | 用途 |
|------|------|------|
| `deploy-arm64.sh` | 主部署脚本 | 自动化部署和配置 |
| `quick-start-arm64.sh` | 快速安装脚本 | 系统环境准备和安装 |
| `health-check.sh` | 健康检查工具 | 服务监控和性能分析 |
| `agentscope.service` | 系统服务配置 | systemd 服务集成 |
| `ARM64-DEPLOYMENT.md` | 详细部署文档 | 完整的使用说明 |

## 🎯 快速开始

### 方式一：一键部署（推荐）

```bash
# 1. 确保你有 agentscope-initializr-arm64.tar.gz 文件
# 2. 运行部署脚本
./deploy-arm64.sh
```

### 方式二：全新安装

```bash
# 在 ARM64 机器上运行
./quick-start-arm64.sh
```

### 方式三：手动部署

```bash
# 1. 加载镜像
docker load -i agentscope-initializr-arm64.tar.gz

# 2. 运行部署脚本
./deploy-arm64.sh
```

## 🛠️ 部署后管理

### 服务管理

```bash
./manage.sh              # 查看所有可用命令
./manage.sh start        # 启动服务
./manage.sh stop         # 停止服务
./manage.sh restart      # 重启服务
./manage.sh logs         # 查看日志
./manage.sh status       # 检查状态
./manage.sh health       # 健康检查
./manage.sh shell        # 进入容器
```

### 健康监控

```bash
./health-check.sh        # 基本健康检查
./health-check.sh --full # 完整检查（含性能分析）
./health-check.sh --monitor  # 持续监控模式
```

## 🌐 访问服务

部署完成后：

- **主页**: http://your-server-ip:8000
- **API文档**: http://your-server-ip:8000/docs
- **健康检查**: http://your-server-ip:8000/health

## 📋 部署流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 系统检查                                              │
│     ├─ 依赖检查 (Docker, Docker Compose)                │
│     ├─ 架构验证 (ARM64)                                  │
│     └─ 权限确认                                          │
├─────────────────────────────────────────────────────────┤
│  2. 镜像处理                                              │
│     ├─ 查找镜像文件                                      │
│     ├─ 加载 Docker 镜像                                 │
│     └─ 验证镜像完整性                                    │
├─────────────────────────────────────────────────────────┤
│  3. 配置生成                                              │
│     ├─ Docker Compose 配置                              │
│     ├─ 管理脚本                                          │
│     └─ 必要目录                                          │
├─────────────────────────────────────────────────────────┤
│  4. 服务启动                                              │
│     ├─ 启动容器                                          │
│     ├─ 健康检查                                          │
│     └─ 服务验证                                          │
└─────────────────────────────────────────────────────────┘
```

## 🔧 系统要求

- **架构**: ARM64 (aarch64)
- **操作系统**: Linux (Ubuntu/Debian/CentOS/RHEL)
- **依赖**:
  - Docker 20.10+
  - Docker Compose 2.0+
- **内存**: 最低 512MB，推荐 2GB+
- **磁盘**: 最低 500MB 可用空间

## 📊 监控和维护

### 日志管理

```bash
# 实时查看日志
docker-compose -f docker-compose.arm64.yml logs -f

# 导出日志
docker-compose -f docker-compose.arm64.yml logs > app.log
```

### 数据备份

```bash
# 备份输出目录
tar -czf backup-$(date +%Y%m%d).tar.gz ./output/

# 恢复数据
tar -xzf backup-20260410.tar.gz
```

### 性能监控

```bash
# 容器资源使用
docker stats agentscope-initializr

# 详细健康检查
./health-check.sh --full
```

## 🔐 生产环境建议

### 1. 配置防火墙

```bash
# UFW
sudo ufw allow 8000/tcp

# firewalld
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 2. 设置系统服务

```bash
# 启用开机自启
sudo systemctl enable agentscope.service

# 启动服务
sudo systemctl start agentscope.service

# 查看状态
sudo systemctl status agentscope.service
```

### 3. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 故障排查

### 服务启动失败

```bash
# 查看详细日志
./manage.sh logs

# 检查容器状态
./manage.sh status

# 检查端口占用
sudo lsof -i :8000
```

### 健康检查失败

```bash
# 运行完整健康检查
./health-check.sh --full

# 进入容器调试
./manage.sh shell
```

### 镜像加载问题

```bash
# 手动加载镜像
docker load -i agentscope-initializr-arm64.tar.gz

# 查看镜像
docker images | grep agentscope
```

## 📈 性能优化

### 资源限制

编辑 `docker-compose.arm64.yml`：

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 4G
```

### 启用多进程

修改容器启动命令使用多 worker。

### 配置缓存

添加 Redis 服务进行缓存。

## 🆘 获取帮助

- 详细文档: `ARM64-DEPLOYMENT.md`
- API 文档: http://your-server:8000/docs
- 健康检查: http://your-server:8000/health

## 📝 更新日志

- **v1.0** (2026-04-10)
  - 初始版本
  - 一键部署功能
  - 健康监控工具
  - 管理脚本集成

---

**提示**: 首次部署建议在测试环境验证，确认无误后再部署到生产环境。

有问题？查看 `ARM64-DEPLOYMENT.md` 获取详细说明。
