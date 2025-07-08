#!/bin/bash

# Agentic Architect Platform - Service Stop Script
# This script stops all running services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_status "🛑 Stopping Agentic Architect Platform Services..."

# Stop services using PID files
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill $FRONTEND_PID 2>/dev/null; then
        print_success "Frontend service stopped (PID: $FRONTEND_PID)"
    else
        print_warning "Frontend service was not running or already stopped"
    fi
    rm -f logs/frontend.pid
fi

if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill $BACKEND_PID 2>/dev/null; then
        print_success "Backend service stopped (PID: $BACKEND_PID)"
    else
        print_warning "Backend service was not running or already stopped"
    fi
    rm -f logs/backend.pid
fi

if [ -f logs/agent_service.pid ]; then
    AGENT_PID=$(cat logs/agent_service.pid)
    if kill $AGENT_PID 2>/dev/null; then
        print_success "Agent service stopped (PID: $AGENT_PID)"
    else
        print_warning "Agent service was not running or already stopped"
    fi
    rm -f logs/agent_service.pid
fi

# Force kill any remaining processes
print_status "Cleaning up any remaining processes..."
pkill -f "npm start" 2>/dev/null && print_success "Stopped remaining npm processes" || true
pkill -f "npx serve" 2>/dev/null && print_success "Stopped remaining serve processes" || true
pkill -f "serve -s build" 2>/dev/null && print_success "Stopped remaining serve processes" || true
pkill -f "python3 main.py" 2>/dev/null && print_success "Stopped remaining Python processes" || true
pkill -f "node.*dist/server" 2>/dev/null && print_success "Stopped remaining Node server processes" || true

# Wait a moment for processes to terminate
sleep 3

# Check if ports are still in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $1 is still in use"
        return 1
    else
        print_success "Port $1 is free"
        return 0
    fi
}

print_status "Checking if ports are free..."
check_port 3000  # Frontend
check_port 3001  # Backend
check_port 8000  # Agent Service

print_success "🏁 All services have been stopped!"
echo ""
echo "📊 Service Status: STOPPED"
echo "🔄 To restart: ./start_services.sh"
echo "📋 To view logs: tail -f logs/*.log"
echo ""
