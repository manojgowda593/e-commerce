#!/usr/bin/env python3
import subprocess
import sys
import time

services = [
    {'name': 'API Gateway', 'dir': 'api_gateway', 'port': 8000},
    {'name': 'User Service', 'dir': 'user_service', 'port': 8001},
    {'name': 'Product Service', 'dir': 'product_service', 'port': 8002},
    {'name': 'Order Service', 'dir': 'order_service', 'port': 8003},
    {'name': 'UI Service', 'dir': 'ui_service', 'port': 8080},
]

print('\033[1m\033[36m🚀 Starting Django microservices...\033[0m\n')

processes = []

for service in services:
    print(f"Starting {service['name']} on port {service['port']}...")
    proc = subprocess.Popen(
        ['python3', 'manage.py', 'runserver', str(service['port'])],
        cwd=service['dir'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(proc)
    time.sleep(1)

print('\n\033[1m\033[32m✅ All services started!\033[0m')
print('\033[33m📱 Open http://localhost:8080 in your browser\033[0m\n')
print('Press Ctrl+C to stop all services\n')

try:
    for proc in processes:
        proc.wait()
except KeyboardInterrupt:
    print('\n\nStopping all services...')
    for proc in processes:
        proc.terminate()
    print('All services stopped.')
