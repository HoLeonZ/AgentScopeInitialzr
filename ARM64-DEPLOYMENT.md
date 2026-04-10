# ARM64 优雅部署指南

## 🚀 快速开始

### 一键部署

```bash
# 1. 将 arm64.tar.gz 包放到项目目录
cp agentscope-initializr-arm64.tar.gz /path/to/agentscope-initializr/

# 2. 运行部署脚本
chmod +x deploy-arm64.sh
./deploy-arm64.sh
```

就这么简单！脚本会自动完成所有配置。

## 📋 部署特性

✨ **自动化部署**
- 自动检测系统依赖
- 智能查找镜像文件
- 自动生成配置文件
- 健康检查和验证

🎨 **优雅的界面**
- 彩色终端输出
- 进度指示器
- 清晰的步骤提示
- 详细的状态信息

🔧 **完整的管理工具**
- 服务管理脚本
- 日志查看
- 健康检查
- 容器操作

## 📦 部署后结构

```
agentscope-initializr/
├── docker-compose.arm64.yml    # 自动生成的 Docker Compose 配置
├── manage.sh                    # 服务管理脚本
├── output/                      # 持久化输出目录
├── logs/                        # 日志目录
└── deploy-arm64.sh             # 部署脚本
```

## 🛠️ 管理命令

部署完成后，使用 `manage.sh` 脚本管理服务：

```bash
# 启动服务
./manage.sh start

# 停止服务
./manage.sh stop

# 重启服务
./manage.sh restart

# 查看日志
./manage.sh logs

# 检查状态
./manage.sh status

# 健康检查
./manage.sh health

# 进入容器
./manage.sh shell

# 清理数据（谨慎使用）
./manage.sh clean
```

## 🌐 访问服务

部署成功后，可以通过以下地址访问：

- **主页**: `http://your-server-ip:8000`
- **API 文档**: `http://your-server-ip:8000/docs`
- **健康检查**: `http://your-server-ip:8000/health`

## 🔍 故障排查

### 服务启动失败

```bash
# 查看详细日志
docker-compose -f docker-compose.arm64.yml logs -f

# 检查容器状态
docker-compose -f docker-compose.arm64.yml ps

# 检查端口占用
sudo lsof -i :8000
```

### 镜像加载失败

```bash
# 手动加载镜像
docker load -i agentscope-initializr-arm64.tar.gz

# 查看镜像列表
docker images | grep agentscope
```

### 权限问题

```bash
# 修复输出目录权限
sudo chown -R $USER:$USER ./output/
chmod -R 755 ./output/
```

## 🚀 高级配置

### 自定义端口

编辑 `docker-compose.arm64.yml`：

```yaml
ports:
  - "8080:8000"  # 将容器端口 8000 映射到主机端口 8080
```

### 设置环境变量

```yaml
environment:
  - LOG_LEVEL=debug
  - OUTPUT_DIR=/app/output
  - CUSTOM_ENV=value
```

### 配置资源限制

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 1G
```

## 🔐 生产环境建议

### 1. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. 配置防火墙

```bash
# UFW
sudo ufw allow 8000/tcp
sudo ufw enable

# firewalld
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 3. 设置系统服务

创建 `/etc/systemd/system/agentscope.service`：

```ini
[Unit]
Description=AgentScope Initializr
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/agentscope-initializr
ExecStart=/usr/local/bin/docker-compose -f docker-compose.arm64.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.arm64.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable agentscope.service
sudo systemctl start agentscope.service
```

## 📊 监控和维护

### 日志管理

```bash
# 查看实时日志
docker-compose -f docker-compose.arm64.yml logs -f

# 导出日志
docker-compose -f docker-compose.arm64.yml logs > app.log

# 清理日志
docker-compose -f docker-compose.arm64.yml logs --tail=0 -f
```

### 数据备份

```bash
# 备份输出目录
tar -czf backup-$(date +%Y%m%d).tar.gz ./output/

# 恢复数据
tar -xzf backup-20260410.tar.gz
```

### 定期维护

```bash
# 清理未使用的 Docker 资源
docker system prune -a

# 更新镜像
docker load -i new-agentscope-initializr-arm64.tar.gz
./manage.sh restart
```

## 🎯 性能优化

### 1. 启用多进程

修改 `CMD` 指令使用多 worker：

```bash
CMD ["uvicorn", "initializr_web.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 2. 配置缓存

添加 Redis 缓存服务到 `docker-compose.arm64.yml`。

### 3. 负载均衡

使用多个容器实例和 Nginx 负载均衡。

## 📞 支持

如有问题，请查看：
- 项目文档：`docs/deployment-guide.md`
- API 文档：`http://your-server:8000/docs`
- 健康检查：`http://your-server:8000/health`

---

**提示**: 首次部署建议在测试环境验证，确认无误后再部署到生产环境。
