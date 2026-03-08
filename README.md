# Django Microservices Application

A microservices architecture built with Django featuring 3 independent services and a web UI, designed for deployment with Emissary (Ambassador) API Gateway in EKS.

## Architecture

- **User Service** (Port 8001) - Manages user data
- **Product Service** (Port 8002) - Handles product catalog
- **Order Service** (Port 8003) - Processes orders
- **UI Service** (Port 8080) - Web interface
- **Emissary** - API Gateway / Ingress Controller (handles routing)

## Installation

### Prerequisites
- Docker
- Docker Compose

## Running the Application

### Using Docker Compose (Recommended)

1. Build and start all services:
```bash
docker-compose up --build
```

2. Or run in detached mode:
```bash
docker-compose up -d
```

3. Stop all services:
```bash
docker-compose down
```

### Option 1: Run Locally (Recommended for first run)

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Start all services using Python script:
```bash
python3 start_all.py
```

Or use the bash script:
```bash
chmod +x start_all.sh
./start_all.sh
```

Or run services individually in separate terminals:
```bash
# Terminal 1 - User Service
cd user_service && python3 manage.py runserver 8001

# Terminal 2 - Product Service
cd product_service && python3 manage.py runserver 8002

# Terminal 3 - Order Service
cd order_service && python3 manage.py runserver 8003

# Terminal 4 - UI Service
cd ui_service && python3 manage.py runserver 8080
```

### Option 2: Using Docker Compose

1. Build and start all services:
```bash
docker-compose up --build
```

2. Or run in detached mode:
```bash
docker-compose up -d
```

3. Stop all services:
```bash
docker-compose down
```

### Option 3: Run Services Independently with Docker

## Access

Open your browser and navigate to:
```
http://localhost:8080
```

## API Endpoints

All requests go through the API Gateway at `http://localhost:8000/api`

- GET `/api/user/` - List all users
- GET `/api/user/<id>/` - Get specific user
- POST `/api/user/` - Create new user
- GET `/api/product/` - List all products
- GET `/api/product/<id>/` - Get specific product
- POST `/api/product/` - Create new product
- GET `/api/order/` - List all orders
- GET `/api/order/<id>/` - Get specific order
- POST `/api/order/` - Create new order

## Features

- Built with Django and Django REST Framework
- No database required (in-memory storage)
- 3 independent microservices
- API Gateway pattern with request proxying
- CORS enabled for cross-origin requests
- Modern responsive UI
- RESTful APIs
- Each service has its own Dockerfile for independent deployment

## Technology Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.0
- Requests 2.31.0
- Docker & Docker Compose

## Docker Commands

### Run All Services Together
```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild a specific service
docker-compose build user-service

# Restart a specific service
docker-compose restart user-service
```

### Run Services Independently
Each service has its own Dockerfile and can be run independently:

```bash
# Create a shared network first
docker network create microservices-network

# Run each service independently
cd user_service && docker build -t user-service . && docker run --network microservices-network --name user-service -p 8001:8001 user-service

cd product_service && docker build -t product-service . && docker run --network microservices-network --name product-service -p 8002:8002 product-service

cd order_service && docker build -t order-service . && docker run --network microservices-network --name order-service -p 8003:8003 order-service

cd api_gateway && docker build -t api-gateway . && docker run --network microservices-network --name api-gateway -p 8000:8000 api-gateway

cd ui_service && docker build -t ui-service . && docker run --network microservices-network --name ui-service -p 8080:8080 ui-service
```
