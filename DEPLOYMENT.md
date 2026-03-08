# EKS Deployment Guide

## Architecture Overview

This microservices application is designed to run as separate containers in Amazon EKS (Elastic Kubernetes Service).

## Request Flow in EKS

```
Internet/User
    ↓
AWS Load Balancer (ALB/NLB)
    ↓
    ├─→ UI Service (Port 8080) - Serves HTML pages
    │   When user clicks button, JavaScript makes API call ↓
    │
    └─→ API Gateway (Port 8000) - Handles /api/* requests
        ↓
        ├─→ User Service (Port 8001)
        ├─→ Product Service (Port 8002)
        └─→ Order Service (Port 8003)
```

### Detailed Request Flow:

**1. Initial Page Load (HTML)**
```
User Browser → ALB → UI Service (Port 8080)
Returns: HTML page (index.html, users.html, products.html, orders.html)
```

**2. User Clicks Button (API Call)**
```
Browser JavaScript → ALB → API Gateway (Port 8000) → Microservice
Returns: JSON data
```

**Example Flow:**
1. User opens `http://your-alb-url.amazonaws.com` → ALB → UI Service → Returns home page
2. User clicks "Users" button → ALB → UI Service → Returns users.html
3. User clicks "Load Users" → JavaScript fetch() → ALB → API Gateway → User Service → Returns JSON
4. Browser displays the JSON data

### Two Types of Requests:

**Type 1: Page Requests (HTML)**
- `/` → UI Service → index.html
- `/users/` → UI Service → users.html
- `/products/` → UI Service → products.html
- `/orders/` → UI Service → orders.html

**Type 2: API Requests (JSON)**
- `/api/user/` → API Gateway → User Service → JSON
- `/api/product/` → API Gateway → Product Service → JSON
- `/api/order/` → API Gateway → Order Service → JSON

## Container Configuration

Each service runs in its own container with:
- Independent Dockerfile
- Separate deployment
- Own Kubernetes Service for internal communication
- No need for service-to-service environment variables (Emissary handles routing)

## Service Discovery in EKS

Services are discovered by Kubernetes DNS:
- `http://user-service:8001` - User Service
- `http://product-service:8002` - Product Service
- `http://order-service:8003` - Order Service
- `http://ui-service:8080` - UI Service

Emissary routes requests to these services based on URL paths.

## Environment Variables for EKS

### All Services (Simplified)
```bash
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*
PORT=8001  # or 8002, 8003, 8080 depending on service
```

No need for service URLs since Emissary handles routing!

## Docker Images

Build and push images to ECR (Elastic Container Registry):

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build images (4 services, no API Gateway)
docker build -t user-service ./user_service
docker build -t product-service ./product_service
docker build -t order-service ./order_service
docker build -t ui-service ./ui_service

# Tag images
docker tag user-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/user-service:latest
docker tag product-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/product-service:latest
docker tag order-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/order-service:latest
docker tag ui-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ui-service:latest

# Push images
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/user-service:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/product-service:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/order-service:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ui-service:latest
```

## Kubernetes Resources Needed

For each service, you'll need:

1. **Deployment** - Runs the container pods
2. **Service** - Exposes the deployment internally (ClusterIP)
3. **Ingress/LoadBalancer** - Exposes UI Service externally

### Service Types:
- **UI Service**: LoadBalancer or Ingress (external access)
- **API Gateway**: ClusterIP (internal only)
- **User Service**: ClusterIP (internal only)
- **Product Service**: ClusterIP (internal only)
- **Order Service**: ClusterIP (internal only)

## Scaling

Each microservice can be scaled independently:
```bash
kubectl scale deployment user-service --replicas=3
kubectl scale deployment product-service --replicas=5
kubectl scale deployment order-service --replicas=2
```

## Health Checks

Add health check endpoints to each service for Kubernetes liveness/readiness probes.

## Networking

- All services communicate within the same Kubernetes cluster
- Emissary handles all external traffic routing
- All services use ClusterIP (internal only)
- Emissary is exposed via ALB/LoadBalancer
- No database required (in-memory storage)

## Security Considerations

1. Use Kubernetes Secrets for sensitive data
2. Implement Network Policies to restrict pod-to-pod communication
3. Use IAM roles for service accounts (IRSA)
4. Enable pod security policies
5. Use private subnets for microservices
6. Expose only UI Service publicly

## Monitoring

- Use CloudWatch Container Insights for EKS monitoring
- Implement logging with Fluentd/CloudWatch Logs
- Add Prometheus metrics endpoints
- Use AWS X-Ray for distributed tracing
