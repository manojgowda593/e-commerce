# Complete Request Flow in EKS

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Internet/User                            │
│                    (Browser: Chrome, Firefox)                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTP Request
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  AWS Application Load Balancer (ALB)             │
│                  URL: http://your-alb-url.amazonaws.com          │
│                  - Routes ALL traffic to UI Service              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Forwards to UI Service
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      UI Service Container                        │
│                         (Port 8080)                              │
│                    Type: LoadBalancer Service                    │
│                                                                  │
│  Serves HTML Pages:                                              │
│  - GET /           → index.html (Home page with buttons)        │
│  - GET /users/     → users.html (User management page)          │
│  - GET /products/  → products.html (Product catalog page)       │
│  - GET /orders/    → orders.html (Order management page)        │
│                                                                  │
│  Each HTML page contains JavaScript that makes API calls        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ User clicks button in browser
                             │ JavaScript makes fetch() call
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              Browser JavaScript (Client-Side)                    │
│                                                                  │
│  fetch('http://your-alb-url.amazonaws.com/api/user/')           │
│  fetch('http://your-alb-url.amazonaws.com/api/product/')        │
│  fetch('http://your-alb-url.amazonaws.com/api/order/')          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ API Request goes back through ALB
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  AWS Application Load Balancer (ALB)             │
│                  - Receives /api/* requests                      │
│                  - Routes to API Gateway Service                 │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Forwards to API Gateway
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   API Gateway Container                          │
│                        (Port 8000)                               │
│                   Type: ClusterIP Service                        │
│                                                                  │
│  Routes based on URL path:                                       │
│  - /api/user/*    → http://user-service:8001                    │
│  - /api/product/* → http://product-service:8002                 │
│  - /api/order/*   → http://order-service:8003                   │
│                                                                  │
│  Acts as a reverse proxy                                         │
└────────────────────────────┬─────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│User Service  │    │Product Service│   │Order Service │
│ (Port 8001)  │    │ (Port 8002)   │   │ (Port 8003)  │
│              │    │               │   │              │
│ClusterIP     │    │ClusterIP      │   │ClusterIP     │
│              │    │               │   │              │
│Returns JSON  │    │Returns JSON   │   │Returns JSON  │
└──────┬───────┘    └──────┬────────┘   └──────┬───────┘
       │                   │                    │
       └───────────────────┼────────────────────┘
                           │
                           │ Response (JSON data)
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   API Gateway Container                          │
│                   Returns JSON to browser                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ JSON Response
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  AWS Application Load Balancer (ALB)             │
│                  Forwards response to browser                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTP Response
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      User's Browser                              │
│              JavaScript displays the JSON data                   │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Step-by-Step Flow

### Step 1: Initial Page Load
```
User → ALB → UI Service (Port 8080)
```
- User opens browser and goes to: `http://your-alb-url.amazonaws.com`
- ALB routes request to UI Service
- UI Service returns `index.html` (home page with 3 buttons)
- Browser displays the home page

### Step 2: User Clicks "Users" Button
```
Browser → ALB → UI Service (Port 8080)
```
- User clicks "Users" button
- Browser navigates to: `http://your-alb-url.amazonaws.com/users/`
- ALB routes to UI Service
- UI Service returns `users.html`
- Browser displays the users page with "Load All Users" button

### Step 3: User Clicks "Load All Users" Button
```
Browser JavaScript → ALB → API Gateway (Port 8000) → User Service (Port 8001)
```
- User clicks "Load All Users" button
- JavaScript executes: `fetch('http://your-alb-url.amazonaws.com/api/user/')`
- Request goes: Browser → ALB → API Gateway
- API Gateway sees `/api/user/` and routes to: `http://user-service:8001/user/`
- User Service returns JSON: `[{id: 1, name: "John"}, {id: 2, name: "Jane"}]`
- Response flows back: User Service → API Gateway → ALB → Browser
- JavaScript displays the JSON data on the page

### Step 4: Similar Flow for Products
```
Browser → ALB → UI Service → Returns products.html
Browser JavaScript → ALB → API Gateway → Product Service → Returns JSON
```

### Step 5: Similar Flow for Orders
```
Browser → ALB → UI Service → Returns orders.html
Browser JavaScript → ALB → API Gateway → Order Service → Returns JSON
```

## Two Types of Requests

### Type 1: Page Requests (HTML)
```
Browser → ALB → UI Service (Port 8080)
Returns: HTML pages
```
- `/` → index.html
- `/users/` → users.html
- `/products/` → products.html
- `/orders/` → orders.html

### Type 2: API Requests (JSON Data)
```
Browser JavaScript → ALB → API Gateway (Port 8000) → Microservice
Returns: JSON data
```
- `/api/user/` → User Service → JSON
- `/api/product/` → Product Service → JSON
- `/api/order/` → Order Service → JSON

## ALB Configuration Needed

You need to configure ALB with path-based routing:

```yaml
# ALB Ingress or Target Groups configuration
Rules:
  - Path: /api/*
    Target: API Gateway Service (Port 8000)
  
  - Path: /*
    Target: UI Service (Port 8080)
```

## Alternative: Single Entry Point

If you want ALL traffic to go through UI Service first:

```
ALB → UI Service (Port 8080)
  ├─ Serves HTML pages (/, /users/, /products/, /orders/)
  └─ Proxies /api/* requests to API Gateway internally
```

But the current design is better because:
1. **Separation of Concerns**: UI serves pages, API Gateway handles API
2. **Better Performance**: Direct API calls don't go through UI service
3. **Easier Scaling**: Scale UI and API independently

## Kubernetes Service Types

```yaml
# UI Service - Exposed externally via ALB
apiVersion: v1
kind: Service
metadata:
  name: ui-service
spec:
  type: LoadBalancer  # Creates ALB
  ports:
  - port: 80
    targetPort: 8080

# API Gateway - Internal only, but accessible via ALB path routing
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: ClusterIP  # Internal only
  ports:
  - port: 8000
    targetPort: 8000

# Microservices - Internal only
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  type: ClusterIP  # Internal only
  ports:
  - port: 8001
    targetPort: 8001
```

## Summary

**YES, you are correct!**

1. ✅ ALB receives ALL requests from internet
2. ✅ Page requests (/, /users/, /products/, /orders/) → UI Container (Port 8080)
3. ✅ API requests (/api/user/, /api/product/, /api/order/) → API Gateway Container (Port 8000)
4. ✅ API Gateway routes to appropriate microservice (User/Product/Order)
5. ✅ Microservices are internal only (ClusterIP), not exposed to internet

The key is that the browser makes TWO types of requests:
- **HTML requests** go to UI Service
- **API requests** (from JavaScript) go to API Gateway
