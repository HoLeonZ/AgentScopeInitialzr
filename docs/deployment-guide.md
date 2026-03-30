# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- (Optional) Kubernetes cluster for K8s deployment
- (Optional) Nginx for production reverse proxy

---

## Development Deployment

### Local Development (Frontend + Backend)

#### 1. Backend Setup

```bash
# Navigate to project root
cd agentscope-initializr

# Install dependencies
pip install -e ".[web,dev]"

# Run development server
cd initializr-web
uvicorn initializr_web.api:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000
API docs at http://localhost:8000/docs

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd initializr-web/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at http://localhost:5173

---

## Docker Deployment

### Quick Start with Docker Compose

#### 1. Build and Start Services

```bash
# From project root
docker-compose up -d
```

This will:
- Build the Docker image
- Start the container on port 8000
- Mount `./output` directory for persistent storage
- Configure health checks

#### 2. Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Test health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.2.0"
}
```

#### 3. Stop Services

```bash
docker-compose down
```

---

## Production Deployment

### Option 1: Docker with Nginx Reverse Proxy

#### Architecture

```
Internet → Nginx (443) → FastAPI App (8000)
               ↓
         Static Files
```

#### 1. Dockerfile Configuration

The project includes a multi-stage Dockerfile:

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
# ... (see Dockerfile)

# Stage 2: Runtime
FROM python:3.11-slim
# ... (see Dockerfile)
```

#### 2. Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Upstream FastAPI
    upstream fastapi {
        server localhost:8000;
    }

    server {
        listen 443 ssl http2;
        server_name api.agentscope-initializr.dev;

        # SSL certificates
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://fastapi/health;
            access_log off;
        }

        # Frontend static files
        location / {
            root /var/www/frontend;
            try_files $uri $uri/ /index.html;
        }
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name api.agentscope-initializr.dev;
        return 301 https://$server_name$request_uri;
    }
}
```

#### 3. Docker Compose for Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  agentscope-api:
    build: .
    container_name: agentscope-api
    restart: always
    environment:
      - LOG_LEVEL=info
      - OUTPUT_DIR=/app/output
      - ALLOW_ORIGINS=https://agentscope-initializr.dev
    volumes:
      - ./output:/app/output
    expose:
      - "8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    container_name: agentscope-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./initializr-web/frontend/dist:/var/www/frontend:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - agentscope-api
```

#### 4. Deploy

```bash
# Build frontend first
cd initializr-web/frontend
npm install
npm run build

# Deploy with production compose
cd ../..
docker-compose -f docker-compose.prod.yml up -d
```

---

### Option 2: Kubernetes Deployment

#### 1. Namespace

Create `namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: agentscope-initializr
```

#### 2. Deployment

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentscope-api
  namespace: agentscope-initializr
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentscope-api
  template:
    metadata:
      labels:
        app: agentscope-api
    spec:
      containers:
      - name: api
        image: agentscope-initializr:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: LOG_LEVEL
          value: "info"
        - name: OUTPUT_DIR
          value: "/app/output"
        - name: ALLOW_ORIGINS
          value: "https://agentscope-initializr.dev"
        volumeMounts:
        - name: output
          mountPath: /app/output
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: output
        persistentVolumeClaim:
          claimName: output-pvc
```

#### 3. Service

Create `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agentscope-api
  namespace: agentscope-initializr
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  selector:
    app: agentscope-api
```

#### 4. Ingress

Create `ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agentscope-ingress
  namespace: agentscope-initializr
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.agentscope-initializr.dev
    secretName: agentscope-tls
  rules:
  - host: api.agentscope-initializr.dev
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: agentscope-api
            port:
              number: 80
      - path: /health
        pathType: Exact
        backend:
          service:
            name: agentscope-api
            port:
              number: 80
```

#### 5. Persistent Volume Claim

Create `pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: output-pvc
  namespace: agentscope-initializr
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

#### 6. Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n agentscope-initializr
kubectl get services -n agentscope-initializr
kubectl get ingress -n agentscope-initializr

# Check logs
kubectl logs -f deployment/agentscope-api -n agentscope-initializr
```

---

## Cloud Platform Deployment

### AWS ECS

#### 1. Push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t agentscope-initializr .

# Tag image
docker tag agentscope-initializr:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentscope-initializr:latest

# Push image
docker push \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentscope-initializr:latest
```

#### 2. ECS Task Definition

```json
{
  "family": "agentscope-initializr",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "agentscope-api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/agentscope-initializr:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "info"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

---

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/agentscope-initializr

# Deploy to Cloud Run
gcloud run deploy agentscope-initializr \
  --image gcr.io/PROJECT-ID/agentscope-initializr \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300
```

---

### Azure Container Instances

```bash
# Create resource group
az group create --name agentscope-rg --location eastus

# Create container registry
az acr create --resource-group agentscope-rg \
  --name agentscopeacr --sku Basic

# Build and push image
az acr build --registry agentscopeacr \
  --image agentscope-initializr:latest .

# Deploy container instance
az container create \
  --resource-group agentscope-rg \
  --name agentscope-initializr \
  --image agentscopeacr.azurecr.io/agentscope-initializr:latest \
  --cpu 1 \
  --memory 1 \
  --ports 8000 \
  --dns-name-label agentscope-api
```

---

## Monitoring and Logging

### Health Monitoring

```bash
# Simple health check script
#!/bin/bash
while true; do
  status=$(curl -s http://localhost:8000/health | jq -r '.status')
  if [ "$status" != "healthy" ]; then
    echo "Service unhealthy!" | mail -s "Alert" admin@example.com
  fi
  sleep 60
done
```

### Log Aggregation (Docker)

```bash
# View logs
docker-compose logs -f

# Export logs
docker-compose logs > app.log

# Configure log rotation in docker-compose.yml
services:
  agentscope-api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Prometheus Metrics (Future)

```python
# Add to api.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

---

## Backup and Recovery

### Backup Generated Projects

```bash
# Backup output directory
tar -czf backup-$(date +%Y%m%d).tar.gz ./output/

# Upload to S3
aws s3 cp backup-$(date +%Y%m%d).tar.gz \
  s3://backup-bucket/agentscope-initializr/
```

### Restore from Backup

```bash
# Download from S3
aws s3 cp s3://backup-bucket/agentscope-initializr/backup-20260327.tar.gz ./

# Extract
tar -xzf backup-20260327.tar.gz
```

---

## Security Hardening

### 1. Environment Variables

Never hardcode secrets. Use environment variables:

```yaml
# docker-compose.yml
services:
  agentscope-api:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=info
```

Create `.env` file:

```bash
OPENAI_API_KEY=sk-...
LOG_LEVEL=info
```

### 2. Secrets Management (Kubernetes)

```bash
# Create secret
kubectl create secret generic api-secrets \
  --from-literal=openai-api-key=sk-... \
  -n agentscope-initializr

# Mount in pod
env:
- name: OPENAI_API_KEY
  valueFrom:
    secretKeyRef:
      name: api-secrets
      key: openai-api-key
```

### 3. Network Policies

```yaml
# Kubernetes network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: agentscope-policy
  namespace: agentscope-initializr
spec:
  podSelector:
    matchLabels:
      app: agentscope-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
```

---

## Performance Tuning

### 1. Uvicorn Workers

```bash
# Run with multiple workers
uvicorn initializr_web.api:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### 2. Connection Pooling

```python
# Add to api.py
from asyncio import Semaphore

request_semaphore = Semaphore(100)

@app.middleware("http")
async def limit_concurrency(request: Request, call_next):
    async with request_semaphore:
        return await call_next(request)
```

### 3. Caching (Redis)

```python
# Add Redis caching
import redis
from functools import lru_cache

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@lru_cache(maxsize=100)
def get_cached_templates():
    cached = redis_client.get('templates')
    if cached:
        return json.loads(cached)
    # ... fetch templates
    redis_client.setex('templates', 3600, json.dumps(templates))
    return templates
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 2. Docker Build Failures

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 3. Permission Issues

```bash
# Fix output directory permissions
sudo chown -R $USER:$USER ./output/
chmod -R 755 ./output/
```

#### 4. High Memory Usage

```bash
# Limit container memory
docker-compose up -d --scale agentscope-api=1

# Check resource usage
docker stats
```

---

## Cost Optimization

### AWS Cost Estimate

- **ECS Fargate**: $0.04048 per vCPU-hour
- **2 vCPUs, 4GB RAM**: ~$60/month
- **ALB**: $0.0225 per LCU-hour (~$16/month)
- **EFS Storage**: $0.30 per GB-month
- **Total**: ~$100/month for small deployment

### GCP Cost Estimate

- **Cloud Run**: Pay-per-use
  - 2 vCPUs, 4GB RAM: ~$0.04 per 100K requests
- **Cloud Storage**: $0.026 per GB-month
- **Total**: ~$50/month for moderate traffic

---

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -e ".[web,dev]"

# Rebuild Docker image
docker-compose build

# Restart services
docker-compose up -d
```

### Log Rotation

```bash
# Setup logrotate
cat > /etc/logrotate.d/agentscope << EOF
/var/log/agentscope/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        docker-compose restart agentscope-api
    endscript
}
EOF
```

---

**Document Version**: 1.0
**Last Updated**: 2026-03-27
