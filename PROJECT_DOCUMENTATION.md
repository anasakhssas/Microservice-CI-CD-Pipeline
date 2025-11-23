# Microservice CI/CD Pipeline - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Application Components](#application-components)
6. [Docker Configuration](#docker-configuration)
7. [Kubernetes Deployment](#kubernetes-deployment)
8. [Monitoring System](#monitoring-system)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [Testing Strategy](#testing-strategy)
11. [Deployment Guide](#deployment-guide)
12. [Best Practices](#best-practices)

---

## 1. Project Overview

### 1.1 Introduction
This project demonstrates a complete **microservice architecture** with a full **CI/CD pipeline**, containerization using **Docker**, orchestration with **Kubernetes**, and comprehensive **monitoring** using Prometheus and Grafana.

### 1.2 Objectives
- Build a scalable microservice application using Flask
- Implement containerization for consistent deployment environments
- Configure Kubernetes for production-grade orchestration
- Set up automated CI/CD pipelines for continuous deployment
- Implement monitoring and observability solutions
- Ensure high availability and fault tolerance

### 1.3 Key Features
- **RESTful API** with health checks and data processing endpoints
- **Docker containerization** for portability
- **Kubernetes deployment** with replicas for high availability
- **Automated testing** with pytest
- **Monitoring stack** with Prometheus and Grafana
- **GitLab CI/CD** integration for automated deployments

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Ingress Controller                    │
│                  (your-domain.com)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Service (ClusterIP)              │
│                  microservice-service                    │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │  Pod 1  │ │  Pod 2  │ │  Pod 3  │
    │ Flask   │ │ Flask   │ │ Flask   │
    │ App     │ │ App     │ │ App     │
    │ :5000   │ │ :5000   │ │ :5000   │
    └─────────┘ └─────────┘ └─────────┘
```

### 2.2 Monitoring Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Prometheus    │ ◄────── │  Microservice   │
│   :9090         │ scrapes │  Pods           │
└────────┬────────┘         └─────────────────┘
         │
         │ data source
         ▼
┌─────────────────┐
│    Grafana      │
│    :3000        │
│  (Dashboards)   │
└─────────────────┘
```

### 2.3 CI/CD Pipeline Flow

```
Developer Push → GitLab → CI Pipeline → Build → Test → Deploy
                                         ↓       ↓      ↓
                                      Docker  Pytest  K8s
```

---

## 3. Technology Stack

### 3.1 Backend Framework
- **Flask 2.0.1**: Lightweight Python web framework
  - Easy to set up and configure
  - Perfect for microservices
  - Extensive ecosystem and community support

### 3.2 Containerization
- **Docker**: Application containerization
  - Ensures consistency across environments
  - Simplifies dependency management
  - Enables efficient resource utilization

### 3.3 Orchestration
- **Kubernetes**: Container orchestration platform
  - Automated deployment and scaling
  - Self-healing capabilities
  - Service discovery and load balancing
  - Rolling updates with zero downtime

### 3.4 Monitoring
- **Prometheus**: Metrics collection and storage
  - Time-series database
  - Powerful query language (PromQL)
  - Alert management

- **Grafana**: Visualization and dashboards
  - Real-time monitoring
  - Custom dashboards
  - Alert visualization

### 3.5 CI/CD
- **GitLab CI/CD**: Automation pipeline
  - Automated testing
  - Continuous integration
  - Continuous deployment

### 3.6 Testing
- **pytest 6.2.4**: Python testing framework
  - Simple and scalable test structure
  - Fixtures for test setup
  - Comprehensive assertions

---

## 4. Project Structure

```
microservice-cicd-pipeline/
│
├── app/                          # Application directory
│   ├── Dockerfile               # Container definition
│   ├── src/                     # Source code
│   │   ├── main.py             # Flask application
│   │   └── requirements.txt    # Python dependencies
│   └── tests/                   # Test suite
│       └── test_main.py        # Unit tests
│
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml         # Pod deployment configuration
│   ├── service.yaml            # Service definition
│   └── ingress.yaml            # Ingress routing rules
│
├── monitoring/                  # Monitoring stack
│   ├── docker-compose.monitoring.yml
│   ├── prometheus/
│   │   └── prometheus.yml      # Prometheus configuration
│   └── grafana/
│       └── provisioning/
│           ├── datasources/    # Data source config
│           └── dashboards/     # Dashboard definitions
│
├── docker-compose.yml           # Local development setup
├── .gitignore                  # Git ignore rules
├── .gitlab-ci.yml              # CI/CD pipeline definition
└── README.md                   # Project documentation
```

---

## 5. Application Components

### 5.1 Flask Application (main.py)

#### 5.1.1 Purpose
The core microservice provides RESTful API endpoints for health monitoring and data processing.

#### 5.1.2 Endpoints

**Health Check Endpoint**
```python
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='healthy'), 200
```
- **Purpose**: Monitor application availability
- **Use Case**: Kubernetes liveness and readiness probes
- **Response**: JSON with status indicator
- **HTTP Status**: 200 OK

**Data Processing Endpoint**
```python
@app.route('/data', methods=['POST'])
def process_data():
    data = request.json
    return jsonify(result='Data processed successfully', input=data), 201
```
- **Purpose**: Process incoming data
- **Method**: POST
- **Content-Type**: application/json
- **Response**: Confirmation with echoed input
- **HTTP Status**: 201 Created

#### 5.1.3 Application Configuration
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
- **Host**: `0.0.0.0` - Accessible from outside the container
- **Port**: `5000` - Standard Flask development port
- **Production**: Uses Gunicorn in production environments

### 5.2 Dependencies (requirements.txt)

```
Flask==2.0.1          # Web framework
requests==2.25.1      # HTTP library
pytest==6.2.4         # Testing framework
gunicorn==20.1.0      # WSGI HTTP server (production)
```

**Dependency Analysis:**
- **Flask**: Provides the web server and routing
- **requests**: For making HTTP calls to external services
- **pytest**: Automated testing framework
- **gunicorn**: Production-grade WSGI server with better performance

### 5.3 Testing Suite (test_main.py)

#### 5.3.1 Test Configuration
```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```
- Creates a test client for each test
- Enables testing mode in Flask
- Provides isolated test environment

#### 5.3.2 Test Cases

**Test 1: Health Check**
```python
def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
```
- Verifies endpoint accessibility
- Validates response structure
- Ensures correct HTTP status code

**Test 2: Data Processing**
```python
def test_process_data(client):
    test_payload = {"name": "test", "value": 123}
    response = client.post('/data', 
                          data=json.dumps(test_payload),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['result'] == 'Data processed successfully'
    assert data['input'] == test_payload
```
- Tests POST endpoint functionality
- Validates JSON processing
- Ensures data echo functionality
- Verifies correct HTTP status code

---

## 6. Docker Configuration

### 6.1 Dockerfile Analysis

```dockerfile
FROM python:3.9-slim
```
- **Base Image**: Lightweight Python 3.9
- **Size Optimization**: Uses slim variant (smaller footprint)
- **Security**: Official Python image with regular updates

```dockerfile
WORKDIR /app
```
- Sets working directory inside container
- All subsequent commands execute in this directory
- Organizes container filesystem

```dockerfile
COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```
- **Layer Optimization**: Copies requirements first
- **Cache Efficiency**: Dependencies layer cached separately
- **No Cache**: Reduces image size
- **Build Speed**: Faster rebuilds when code changes

```dockerfile
COPY src/ .
```
- Copies application code
- Separate from dependencies for better caching
- Efficient layer management

```dockerfile
CMD ["python", "main.py"]
```
- Default command when container starts
- Can be overridden at runtime
- Uses Python directly (development mode)

### 6.2 Docker Compose (Development)

```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    networks:
      - app-network
```

**Configuration Breakdown:**
- **Build Context**: Points to app directory
- **Port Mapping**: Exposes container port 5000 to host
- **Networking**: Custom bridge network for service isolation

### 6.3 Multi-Container Setup

The monitoring stack uses a separate compose file:

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
    networks:
      - monitoring
```

**Key Features:**
- **Isolation**: Separate network for monitoring
- **Persistence**: Volume mounts for configuration
- **Scalability**: Easy to add more services

---

## 7. Kubernetes Deployment

### 7.1 Deployment Configuration (deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microservice-app
  labels:
    app: microservice-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: microservice-app
```

**Replica Strategy:**
- **3 Replicas**: High availability
- **Load Distribution**: Traffic spread across pods
- **Fault Tolerance**: Service continues if one pod fails
- **Zero Downtime**: Rolling updates without service interruption

```yaml
  template:
    metadata:
      labels:
        app: microservice-app
    spec:
      containers:
      - name: microservice-app
        image: registry.gitlab.com/your-username/microservice-app:latest
        ports:
        - containerPort: 5000
        env:
        - name: ENVIRONMENT
          value: "production"
```

**Container Specifications:**
- **Image**: From GitLab Container Registry
- **Port**: Exposes 5000 for service communication
- **Environment**: Production configuration
- **Immutable Infrastructure**: New deployments create new pods

### 7.2 Service Configuration (service.yaml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: microservice-service
  labels:
    app: microservice-app
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 5000
  selector:
    app: microservice-app
```

**Service Details:**
- **Type**: ClusterIP (internal only)
- **Port Mapping**: External 80 → Internal 5000
- **Selector**: Routes to pods with matching labels
- **Load Balancing**: Automatic distribution across healthy pods

**Why ClusterIP?**
- Internal service not exposed externally
- Ingress controller handles external traffic
- More secure architecture
- Easier to manage SSL/TLS at ingress level

### 7.3 Ingress Configuration (ingress.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservice-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: your-domain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: microservice-service
                port:
                  number: 80
```

**Ingress Features:**
- **Domain Routing**: Routes traffic based on hostname
- **Path-Based Routing**: Different paths to different services
- **SSL Termination**: Handle HTTPS at ingress level
- **URL Rewriting**: Modify URLs as needed

**Configuration Notes:**
- Replace `your-domain.com` with actual domain
- Requires ingress controller (e.g., NGINX)
- Can add TLS certificates for HTTPS
- Supports multiple services and paths

---

## 8. Monitoring System

### 8.1 Prometheus Configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'microservice'
    static_configs:
      - targets: ['app:5000']
```

**Prometheus Features:**
- **Scrape Interval**: Collects metrics every 15 seconds
- **Target**: Monitors Flask application
- **Metrics Storage**: Time-series database
- **Query Language**: PromQL for complex queries

**Key Metrics Collected:**
- Request count
- Response times
- Error rates
- Resource usage (CPU, memory)
- Custom application metrics

### 8.2 Grafana Configuration

**Data Source (datasource.yml):**
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
    jsonData:
      timeInterval: "10s"
```

**Grafana Capabilities:**
- **Visualization**: Real-time dashboards
- **Alerting**: Set thresholds and notifications
- **Data Exploration**: Ad-hoc queries
- **Custom Dashboards**: Tailored to your needs

**Default Dashboards:**
- Application performance metrics
- Request/response statistics
- Error rate monitoring
- Resource utilization

### 8.3 Monitoring Best Practices

1. **Set up alerts** for critical metrics
2. **Create runbooks** for common issues
3. **Monitor trends** over time
4. **Set SLAs** and track compliance
5. **Regular review** of metrics and dashboards

---

## 9. CI/CD Pipeline

### 9.1 GitLab CI/CD Stages

The `.gitlab-ci.yml` file defines the automated pipeline:

**Stage 1: Build**
- Builds Docker image
- Tags with commit SHA
- Pushes to container registry
- Validates Dockerfile

**Stage 2: Test**
- Runs pytest suite
- Validates code quality
- Checks test coverage
- Fails pipeline if tests fail

**Stage 3: Deploy**
- Updates Kubernetes deployment
- Applies new image tag
- Performs rolling update
- Validates deployment health

### 9.2 Pipeline Triggers

- **Push to main**: Full pipeline execution
- **Merge requests**: Build and test only
- **Tags**: Deploy to production
- **Manual trigger**: On-demand deployment

### 9.3 Environment Variables

Required secrets in GitLab:
- `CI_REGISTRY_USER`: Container registry username
- `CI_REGISTRY_PASSWORD`: Container registry password
- `KUBE_CONFIG`: Kubernetes cluster configuration

---

## 10. Testing Strategy

### 10.1 Test Levels

**Unit Tests:**
- Individual function testing
- Isolated component verification
- Fast execution
- High coverage

**Integration Tests:**
- API endpoint testing
- Database interactions
- External service mocking
- End-to-end workflows

**Smoke Tests:**
- Basic functionality verification
- Quick health checks
- Post-deployment validation

### 10.2 Test Execution

**Local Testing:**
```bash
cd app
pytest tests/test_main.py -v
```

**Docker Testing:**
```bash
docker-compose up --build
docker-compose run app pytest tests/
```

**CI Pipeline Testing:**
- Automated on every commit
- Results visible in GitLab
- Blocks merges if tests fail

### 10.3 Test Coverage

Target: **80%+ code coverage**
- All endpoints tested
- Error handling verified
- Edge cases covered
- Response validation

---

## 11. Deployment Guide

### 11.1 Local Development Setup

**Step 1: Clone Repository**
```bash
git clone https://github.com/anasakhssas/Microservice-CI-CD-Pipeline.git
cd microservice-cicd-pipeline
```

**Step 2: Install Dependencies**
```bash
cd app/src
pip install -r requirements.txt
```

**Step 3: Run Application**
```bash
python main.py
```

**Step 4: Run Tests**
```bash
cd ../tests
pytest test_main.py -v
```

### 11.2 Docker Deployment

**Build Image:**
```bash
cd app
docker build -t microservice-app .
```

**Run Container:**
```bash
docker run -p 5000:5000 microservice-app
```

**Using Docker Compose:**
```bash
docker-compose up --build
```

**Start Monitoring:**
```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

**Access Services:**
- Application: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### 11.3 Kubernetes Deployment

**Prerequisites:**
- Kubernetes cluster (Minikube, GKE, EKS, AKS)
- kubectl configured
- Docker image pushed to registry

**Step 1: Update Image Reference**
Edit `k8s/deployment.yaml`:
```yaml
image: registry.gitlab.com/YOUR_USERNAME/microservice-app:latest
```

**Step 2: Apply Configurations**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

**Step 3: Verify Deployment**
```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get ingress
```

**Step 4: Check Pod Logs**
```bash
kubectl logs -f deployment/microservice-app
```

**Step 5: Scale Application**
```bash
kubectl scale deployment microservice-app --replicas=5
```

### 11.4 Production Deployment Checklist

- [ ] Environment variables configured
- [ ] Secrets stored securely
- [ ] Resource limits set (CPU, memory)
- [ ] Health checks configured
- [ ] Monitoring alerts set up
- [ ] Backup strategy in place
- [ ] SSL certificates installed
- [ ] Domain DNS configured
- [ ] Logging centralized
- [ ] Security scanning completed

---

## 12. Best Practices

### 12.1 Code Quality

1. **Follow PEP 8** style guidelines
2. **Write docstrings** for functions
3. **Use type hints** for clarity
4. **Keep functions small** and focused
5. **DRY principle**: Don't Repeat Yourself

### 12.2 Docker Best Practices

1. **Use specific tags** instead of `latest`
2. **Multi-stage builds** for smaller images
3. **Minimize layers** in Dockerfile
4. **Don't run as root** user
5. **Use .dockerignore** to exclude files
6. **Scan images** for vulnerabilities

### 12.3 Kubernetes Best Practices

1. **Set resource requests and limits**
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

2. **Configure health probes**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
```

3. **Use namespaces** for isolation
4. **Implement RBAC** for security
5. **Use ConfigMaps** for configuration
6. **Use Secrets** for sensitive data

### 12.4 CI/CD Best Practices

1. **Fast feedback**: Keep pipeline quick
2. **Fail fast**: Catch errors early
3. **Parallel execution**: Run tests concurrently
4. **Automated rollback**: On deployment failure
5. **Environment parity**: Dev/staging/prod similar
6. **Immutable artifacts**: Don't modify after build

### 12.5 Monitoring Best Practices

1. **Four Golden Signals**:
   - Latency
   - Traffic
   - Errors
   - Saturation

2. **Set meaningful alerts**
3. **Avoid alert fatigue**
4. **Monitor dependencies**
5. **Track business metrics**
6. **Regular dashboard reviews**

### 12.6 Security Best Practices

1. **Regular updates**: Keep dependencies current
2. **Scan for vulnerabilities**: Use tools like Snyk, Trivy
3. **Secrets management**: Use HashiCorp Vault, AWS Secrets Manager
4. **Network policies**: Restrict pod communication
5. **Least privilege**: Minimal permissions
6. **Audit logging**: Track all access
7. **TLS everywhere**: Encrypt in transit
8. **Input validation**: Sanitize all inputs

---

## Appendix A: Troubleshooting

### Common Issues and Solutions

**Issue 1: Pod CrashLoopBackOff**
```bash
# Check pod logs
kubectl logs pod-name

# Describe pod for events
kubectl describe pod pod-name

# Common causes:
# - Application crash
# - Missing environment variables
# - Port conflict
# - Resource limits too low
```

**Issue 2: Service Not Accessible**
```bash
# Verify service endpoints
kubectl get endpoints service-name

# Check pod labels match service selector
kubectl get pods --show-labels

# Test service internally
kubectl run test --rm -it --image=busybox -- wget -O- http://service-name
```

**Issue 3: Ingress Not Working**
```bash
# Check ingress controller is running
kubectl get pods -n ingress-nginx

# Verify ingress resource
kubectl describe ingress microservice-ingress

# Check DNS resolution
nslookup your-domain.com
```

**Issue 4: Monitoring Not Collecting Metrics**
```bash
# Check Prometheus targets
curl http://localhost:9090/targets

# Verify app exposing metrics
curl http://app:5000/metrics

# Check network connectivity
docker network inspect monitoring_monitoring
```

---

## Appendix B: Useful Commands

### Docker Commands
```bash
# Build image
docker build -t app-name .

# Run container
docker run -d -p 5000:5000 app-name

# View logs
docker logs container-id

# Execute command in container
docker exec -it container-id bash

# Clean up
docker system prune -a
```

### Kubernetes Commands
```bash
# Get resources
kubectl get all
kubectl get pods -o wide
kubectl get services
kubectl get deployments

# Describe resource
kubectl describe pod pod-name
kubectl describe service service-name

# Logs
kubectl logs pod-name
kubectl logs -f deployment/app-name

# Scale
kubectl scale deployment app --replicas=5

# Update image
kubectl set image deployment/app app=new-image:tag

# Rollback
kubectl rollout undo deployment/app

# Port forward
kubectl port-forward pod/pod-name 5000:5000
```

### Git Commands
```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b feature-branch

# View history
git log --oneline
```

---

## Appendix C: Additional Resources

### Documentation
- Flask: https://flask.palletsprojects.com/
- Docker: https://docs.docker.com/
- Kubernetes: https://kubernetes.io/docs/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/

### Learning Resources
- Kubernetes Patterns (book)
- Docker Deep Dive (book)
- The DevOps Handbook
- Site Reliability Engineering (Google)

### Tools
- kubectl: Kubernetes CLI
- helm: Kubernetes package manager
- k9s: Terminal UI for Kubernetes
- lens: Kubernetes IDE
- docker-compose: Multi-container orchestration

---

## Conclusion

This microservice CI/CD pipeline project demonstrates modern DevOps practices including:

✅ **Containerization** with Docker for consistency
✅ **Orchestration** with Kubernetes for scalability  
✅ **Automation** with GitLab CI/CD for efficiency
✅ **Monitoring** with Prometheus and Grafana for observability
✅ **Testing** with pytest for quality assurance
✅ **Best practices** for security and reliability

The architecture is **production-ready**, **scalable**, and follows **industry standards**. It can be extended with additional features like:

- Service mesh (Istio, Linkerd)
- API gateway (Kong, Ambassador)
- Distributed tracing (Jaeger, Zipkin)
- Log aggregation (ELK stack, Loki)
- Advanced security (OPA, Falco)

---

**Project Repository**: https://github.com/anasakhssas/Microservice-CI-CD-Pipeline

**Author**: Anas Akhssas  
**Date**: November 23, 2025  
**Version**: 1.0

---

*This documentation is maintained as part of the project repository. For updates and contributions, please refer to the GitHub repository.*
