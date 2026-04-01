# Web 并发控制分析

## 当前实现分析

### 1. FastAPI + Uvicorn 并发模型

**当前配置** (initializr-web/initializr_web/main.py):
```python
uvicorn.run(
    "initializr_web.api:app",
    host="0.0.0.0",
    port=8000,
    reload=True,  # 仅开发环境使用
)
```

**并发特性**:
- **异步框架**: FastAPI 基于 `async/await` 语法
- **ASGI 服务器**: Uvicorn 使用异步 I/O，支持高并发
- **默认工作进程**: 单进程 (`workers=1`)
- **并发请求**: 通过事件循环处理多个并发请求

### 2. 并发控制机制

#### 2.1 异步端点处理

```python
@router.post("/api/v1/projects/generate", response_model=ProjectResponse)
async def generate_project_endpoint(
    request: ProjectRequest,
    background_tasks: BackgroundTasks,
) -> ProjectResponse:
    # 异步处理请求
    project_id = generate_project(request, output_dir)

    # 后台任务清理
    background_tasks.add_task(cleanup_projects)

    return ProjectResponse(...)
```

**关键点**:
- 使用 `async def` 声明异步端点
- `generate_project()` 虽然是同步函数，但在异步上下文中运行
- `BackgroundTasks` 用于非阻塞的后台清理

#### 2.2 并发问题识别

**潜在瓶颈**:

1. **CPU 密集型任务阻塞**
```python
# generator.py
def generate_project(request: ProjectRequest, output_dir: Path) -> str:
    # 同步操作，会阻塞事件循环
    metadata = project_request_to_metadata(request)
    generator = ProjectGenerator(output_dir=str(output_dir))
    generated = generator.generate(metadata)  # CPU 密集型
    generated.create_zip()  # I/O 密集型
```

2. **文件系统竞争**
```python
# 多个请求同时生成项目时
project_id = f"{request.name}_{uuid.uuid4().hex[:8]}"
zip_path = output_dir / f"{project_id}.zip"
# 可能出现文件名冲突（虽然概率很低）
```

3. **磁盘空间竞争**
```python
# 多个并发请求同时生成大型项目
# 可能导致磁盘 I/O 竞争和空间不足
```

## 改进方案

### 方案 1: 使用线程池处理 CPU 密集型任务

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# 创建线程池
executor = ThreadPoolExecutor(max_workers=4)

@router.post("/api/v1/projects/generate")
async def generate_project_endpoint(
    request: ProjectRequest,
    background_tasks: BackgroundTasks,
) -> ProjectResponse:
    loop = asyncio.get_event_loop()

    # 在线程池中运行 CPU 密集型任务
    project_id = await loop.run_in_executor(
        executor,
        partial(generate_project, request, output_dir)
    )

    background_tasks.add_task(cleanup_projects)
    return ProjectResponse(...)
```

**优点**:
- 不会阻塞事件循环
- 充分利用多核 CPU
- 实现简单

**缺点**:
- 线程数量有限制
- 需要管理线程池生命周期

### 方案 2: 使用 Celery 任务队列

```python
from celery import Celery
import redis

# 配置 Celery
celery_app = Celery(
    'initializr',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

@celery_app.task
def generate_project_task(request_data, output_dir):
    """后台生成项目"""
    request = ProjectRequest(**request_data)
    return generate_project(request, Path(output_dir))

@router.post("/api/v1/projects/generate")
async def generate_project_endpoint(request: ProjectRequest):
    """提交生成任务"""
    # 提交到任务队列
    task = generate_project_task.delay(
        request.dict(),
        str(output_dir)
    )

    return ProjectResponse(
        success=True,
        message="Project generation started",
        project_id=task.id,
        download_url=f"/api/v1/projects/download/{task.id}"
    )

@router.get("/api/v1/projects/status/{task_id}")
async def get_project_status(task_id: str):
    """查询任务状态"""
    task = generate_project_task.AsyncResult(task_id)

    if task.ready():
        if task.successful():
            return {"status": "completed", "project_id": task.result}
        else:
            return {"status": "failed", "error": str(task.info)}
    else:
        return {"status": "processing"}
```

**优点**:
- 完全异步处理
- 支持任务持久化
- 可以横向扩展 worker
- 内置重试机制

**缺点**:
- 需要额外的 Redis/消息队列服务
- 增加系统复杂度
- 需要监控 Celery worker

### 方案 3: 请求限流 + 队列

```python
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# 请求队列
generation_queue = asyncio.Queue(maxsize=10)
active_tasks = set()
MAX_CONCURRENT_TASKS = 3

async def process_queue():
    """后台处理队列中的任务"""
    while True:
        request, future = await generation_queue.get()

        # 限制并发数
        while len(active_tasks) >= MAX_CONCURRENT_TASKS:
            await asyncio.sleep(0.5)

        task = asyncio.create_task(generate_project_async(request))
        active_tasks.add(task)

        def on_complete(t):
            active_tasks.discard(t)
            generation_queue.task_done()

        task.add_done_callback(on_complete)

# 启动队列处理器
asyncio.create_task(process_queue())

@router.post("/api/v1/projects/generate")
@limiter.limit("5/minute")  # 限流
async def generate_project_endpoint(
    request: ProjectRequest,
    http_request: Request
):
    """加入生成队列"""
    if generation_queue.qsize() >= generation_queue.maxsize:
        raise HTTPException(
            status_code=503,
            detail="Server is busy, please try again later"
        )

    future = asyncio.Future()
    await generation_queue.put((request, future))

    # 等待完成（或返回任务 ID 让用户轮询）
    project_id = await future
    return ProjectResponse(...)
```

**优点**:
- 内存占用低
- 无需额外服务
- 可控的并发数

**缺点**:
- 单点故障（重启丢失队列）
- 需要实现任务持久化（如果需要）

### 方案 4: 使用进程池 + Uvicorn 多 Worker

```python
# uvicorn 启动配置
uvicorn.run(
    "initializr_web.api:app",
    host="0.0.0.0",
    port=8000,
    workers=4,  # 4 个工作进程
    limit_concurrency=100,  # 限制并发连接数
    timeout_keep_alive=30,
)
```

**优点**:
- 充分利用多核
- 配置简单
- Uvicorn 原生支持

**缺点**:
- 每个进程独立内存
- 需要共享存储（如 Redis）来同步状态

## 推荐方案对比

| 方案 | 复杂度 | 可扩展性 | 可靠性 | 适用场景 |
|------|--------|----------|--------|----------|
| 线程池 | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 中小规模 |
| Celery | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 大规模生产环境 |
| 请求队列 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 中等规模 |
| 多 Worker | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 快速部署 |

## 最佳实践建议

### 1. 分阶段实施

**第一阶段（当前）**:
- 实现方案 1：线程池处理
- 添加请求限流
- 监控并发数

**第二阶段（用户增长后）**:
- 引入 Celery 任务队列
- 实现 Redis 缓存
- 添加任务状态查询 API

**第三阶段（大规模）**:
- 水平扩展 Celery workers
- 使用负载均衡
- 实现分布式任务队列

### 2. 监控指标

```python
# 添加监控中间件
from prometheus_client import Counter, Histogram

request_counter = Counter('requests_total', 'Total requests')
generation_duration = Histogram('generation_seconds', 'Project generation time')
active_tasks_gauge = Gauge('active_tasks', 'Active generation tasks')

@generation_duration.time()
async def generate_project_endpoint(...):
    active_tasks_gauge.inc()
    try:
        # ...
    finally:
        active_tasks_gauge.dec()
```

### 3. 资源限制

```python
# 项目配置
MAX_CONCURRENT_GENERATIONS = 3
MAX_PROJECT_SIZE_MB = 100
GENERATION_TIMEOUT_SECONDS = 300
CLEANUP_AFTER_HOURS = 1
```

### 4. 错误处理

```python
# 优雅降级
from fastapi.responses import JSONResponse

@router.exception_handler(ResourceExhausted)
async def resource_exhausted_handler(request, exc):
    return JSONResponse(
        status_code=503,
        content={
            "error": "Service temporarily unavailable",
            "retry_after": 60
        }
    )
```

## 总结

**当前状态**: 使用基本的 FastAPI 异步处理，适合低并发场景

**推荐升级路径**:
1. 短期：添加线程池 + 请求限流
2. 中期：引入 Celery 任务队列
3. 长期：完整微服务架构

**关键原则**:
- 渐进式改进
- 监控驱动优化
- 用户体验优先（超时、重试、状态查询）
