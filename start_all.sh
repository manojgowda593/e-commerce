#!/bin/bash

echo "🚀 Starting Django microservices..."
echo ""

# Start User Service
echo "Starting User Service on port 8001..."
cd user_service && python3 manage.py runserver 8001 &

# Start Product Service
echo "Starting Product Service on port 8002..."
cd product_service && python3 manage.py runserver 8002 &

# Start Order Service
echo "Starting Order Service on port 8003..."
cd order_service && python3 manage.py runserver 8003 &

# Start UI Service
echo "Starting UI Service on port 8080..."
cd ui_service && python3 manage.py runserver 8080 &

echo ""
echo "✅ All services started!"
echo "📱 Open http://localhost:8080 in your browser"
echo ""
echo "Press Ctrl+C to stop all services"

wait
