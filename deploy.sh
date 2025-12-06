#!/bin/bash

# Deployment script for cloud server
# Usage: ./deploy.sh

set -e

echo "=========================================="
echo "ISP Payment Recovery System - Deployment"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    echo "Please install Docker Compose first"
    exit 1
fi

# Create data directory if it doesn't exist
echo "Creating data directory..."
mkdir -p data
chmod 755 data

# Pull latest code (if using git)
if [ -d .git ]; then
    echo "Pulling latest code..."
    git pull || echo "Warning: Could not pull latest code"
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for container to be ready
echo "Waiting for application to start..."
sleep 5

# Check container status
echo ""
echo "Container status:"
docker-compose ps

# Show logs
echo ""
echo "Recent logs:"
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "Application should be running at:"
echo "  - http://localhost:5000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""

