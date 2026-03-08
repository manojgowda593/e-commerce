# ConfigMap Creation Guide for EKS

This guide shows how to create Kubernetes ConfigMaps from the environment files for each microservice.

## Environment Files

Each service has a `.env.example` file:
- `api_gateway/.env.example`
- `user_service/.env.example`
- `product_service/.env.example`
- `order_service/.env.example`
- `ui_service/.env.example`

## Create ConfigMaps from .env files

### Method 1: Create ConfigMap from .env file directly

```bash
# User Service ConfigMap
kubectl create configmap user-service-config \
  --from-env-file=user_service/.env.example \
  -n your-namespace

# Product Service ConfigMap
kubectl create configmap product-service-config \
  --from-env-file=product_service/.env.example \
  -n your-namespace

# Order Service ConfigMap
kubectl create configmap order-service-config \
  --from-env-file=order_service/.env.example \
  -n your-namespace

# UI Service ConfigMap
kubectl create configmap ui-service-config \
  --from-env-file=ui_service/.env.example \
  -n your-namespace
```

### Method 2: Create ConfigMap YAML manually

#### API Gateway ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-gateway-config
  namespace: your-namespace
data:
  DEBUG: "False"
  SECRET_KEY: "change-this-to-a-secure-random-key-in-production"
  ALLOWED_HOSTS: "*"
  USER_SERVICE_URL: "http://user-service:8001"
  PRODUCT_SERVICE_URL: "http://product-service:8002"
  ORDER_SERVICE_URL: "http://order-service:8003"
  CORS_ALLOW_ALL_ORIGINS: "True"
  PORT: "8000"
```

#### User Service ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: user-service-config
  namespace: your-namespace
data:
  DEBUG: "False"
  SECRET_KEY: "change-this-to-a-secure-random-key-in-production"
  ALLOWED_HOSTS: "*"
  CORS_ALLOW_ALL_ORIGINS: "True"
  PORT: "8001"
  SERVICE_NAME: "user-service"
```

#### Product Service ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-service-config
  namespace: your-namespace
data:
  DEBUG: "False"
  SECRET_KEY: "change-this-to-a-secure-random-key-in-production"
  ALLOWED_HOSTS: "*"
  CORS_ALLOW_ALL_ORIGINS: "True"
  PORT: "8002"
  SERVICE_NAME: "product-service"
```

#### Order Service ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
  namespace: your-namespace
data:
  DEBUG: "False"
  SECRET_KEY: "change-this-to-a-secure-random-key-in-production"
  ALLOWED_HOSTS: "*"
  CORS_ALLOW_ALL_ORIGINS: "True"
  PORT: "8003"
  SERVICE_NAME: "order-service"
```

#### UI Service ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ui-service-config
  namespace: your-namespace
data:
  DEBUG: "False"
  SECRET_KEY: "change-this-to-a-secure-random-key-in-production"
  ALLOWED_HOSTS: "*"
  API_GATEWAY_URL: "http://api-gateway:8000"
  PORT: "8080"
  SERVICE_NAME: "ui-service"
```

## Using ConfigMaps in Deployments

Reference the ConfigMap in your deployment YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  template:
    spec:
      containers:
      - name: api-gateway
        image: your-ecr-repo/api-gateway:latest
        envFrom:
        - configMapRef:
            name: api-gateway-config
        # OR use individual env vars:
        env:
        - name: USER_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: api-gateway-config
              key: USER_SERVICE_URL
```

## Verify ConfigMaps

```bash
# List all ConfigMaps
kubectl get configmaps -n your-namespace

# View specific ConfigMap
kubectl describe configmap api-gateway-config -n your-namespace

# Get ConfigMap as YAML
kubectl get configmap api-gateway-config -n your-namespace -o yaml
```

## Update ConfigMaps

```bash
# Edit ConfigMap
kubectl edit configmap api-gateway-config -n your-namespace

# Or delete and recreate
kubectl delete configmap api-gateway-config -n your-namespace
kubectl create configmap api-gateway-config --from-env-file=api_gateway/.env.example -n your-namespace

# Restart pods to pick up new config
kubectl rollout restart deployment api-gateway -n your-namespace
```

## Best Practices

1. **Secrets vs ConfigMaps**
   - Use ConfigMaps for non-sensitive configuration
   - Use Secrets for sensitive data (SECRET_KEY, passwords, API keys)

2. **Environment-Specific ConfigMaps**
   - Create different ConfigMaps for dev, staging, prod
   - Example: `api-gateway-config-dev`, `api-gateway-config-prod`

3. **Version Control**
   - Keep `.env.example` files in git
   - Never commit actual `.env` files with real secrets

4. **Immutable ConfigMaps**
   - Consider making ConfigMaps immutable in production
   - Add `immutable: true` to ConfigMap spec

## Example: Create Secret for SECRET_KEY

```bash
# Create secret for sensitive data
kubectl create secret generic api-gateway-secret \
  --from-literal=SECRET_KEY='your-super-secret-key-here' \
  -n your-namespace

# Reference in deployment
env:
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: api-gateway-secret
      key: SECRET_KEY
```

## All-in-One Script

```bash
#!/bin/bash
NAMESPACE="your-namespace"

# Create all ConfigMaps
kubectl create configmap user-service-config --from-env-file=user_service/.env.example -n $NAMESPACE
kubectl create configmap product-service-config --from-env-file=product_service/.env.example -n $NAMESPACE
kubectl create configmap order-service-config --from-env-file=order_service/.env.example -n $NAMESPACE
kubectl create configmap ui-service-config --from-env-file=ui_service/.env.example -n $NAMESPACE

echo "All ConfigMaps created successfully!"
kubectl get configmaps -n $NAMESPACE
```
