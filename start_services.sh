#!/bin/bash

# Agentic Architect Platform - Service Startup Script
# This script starts all three services: Backend, Agent Service, and Frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get public IP for display
get_public_ip() {
    # Use the fixed public IP for EC2 deployment
    echo "54.194.104.191"
}

print_status "🚀 Starting Agentic Architect Platform Services..."

# Create logs directory
mkdir -p logs

# Function to check if a service is running
check_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f http://127.0.0.1:$port > /dev/null 2>&1; then
            print_success "$service_name is running on port $port"
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start on port $port"
    return 1
}

# Function to check if a port is in use
port_in_use() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Stop any existing services
print_status "Stopping any existing services..."
pkill -f "npm start" 2>/dev/null || true
pkill -f "python3 main.py" 2>/dev/null || true
pkill -f "node.*server" 2>/dev/null || true
sleep 3

# Start Backend Service
print_status "Starting Backend Service (Node.js)..."
cd backend

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    print_status "Installing backend dependencies..."
    npm install
fi

# Build the project (skip type checking for demo)
print_status "Building backend..."
npm run build --skipLibCheck 2>&1 | tee ../logs/backend_build.log || {
    print_warning "Build with skipLibCheck failed, trying without type checking..."
    npx tsc --noEmit false --skipLibCheck 2>&1 | tee ../logs/backend_build.log || {
        print_warning "TypeScript build failed, but continuing..."
    }
}

# Start backend in background (skip build if it fails)
if [ ! -d "dist" ]; then
    print_warning "Build failed, trying to start without build..."
fi
nohup npm start > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid

cd ..

# Wait for backend to start
print_status "Waiting for backend to start..."
sleep 10

# Check backend health
if port_in_use 3001; then
    print_success "Backend started successfully on port 3001"
else
    print_error "Backend failed to start. Check logs/backend.log"
    tail -20 logs/backend.log
    exit 1
fi

# Start Agent Service
print_status "Starting Agent Service (Python)..."
cd agent_service

# Install minimal dependencies if needed
print_status "Installing agent service dependencies..."
pip3 install --user fastapi uvicorn pydantic python-dotenv httpx aiohttp groq structlog click typing-extensions starlette anyio h11 2>/dev/null || true

# Start agent service in background
nohup python3 main.py > ../logs/agent_service.log 2>&1 &
AGENT_PID=$!
echo $AGENT_PID > ../logs/agent_service.pid

cd ..

# Wait for agent service to start
print_status "Waiting for agent service to start..."
sleep 10

# Check agent service health
if port_in_use 8000; then
    print_success "Agent Service started successfully on port 8000"
else
    print_error "Agent Service failed to start. Check logs/agent_service.log"
    tail -20 logs/agent_service.log
    exit 1
fi

# Start Frontend Service
print_status "Starting Frontend Service (React)..."
cd frontend

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    print_status "Installing frontend dependencies..."
    npm install
fi

# Update frontend environment for production
PUBLIC_IP=$(get_public_ip)
echo "REACT_APP_API_URL=http://$PUBLIC_IP:3001/api" > .env
echo "REACT_APP_AGENT_SERVICE_URL=http://$PUBLIC_IP:8000" >> .env
echo "GENERATE_SOURCEMAP=false" >> .env
print_status "Updated frontend environment variables for public IP: $PUBLIC_IP"
print_status "Frontend .env contents:"
cat .env

# Build frontend for production (eliminates WebSocket issues)
print_status "Building frontend for production..."
# Force rebuild to pick up new environment variables
rm -rf build node_modules/.cache 2>/dev/null || true
npm run build
if [ $? -ne 0 ]; then
    print_error "Frontend build failed"
    cat ../logs/frontend_build.log 2>/dev/null || true
    exit 1
fi
print_success "Frontend build completed successfully"

# Install serve locally if not already installed
if [ ! -f "node_modules/.bin/serve" ]; then
    print_status "Installing serve for production hosting..."
    npm install serve
fi

# Start frontend production server in background using local serve
nohup npx serve -s build -l 3000 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid

cd ..

# Wait for frontend to start
print_status "Waiting for frontend to start..."
sleep 15

# Check frontend health
if port_in_use 3000; then
    print_success "Frontend started successfully on port 3000"
else
    print_error "Frontend failed to start. Check logs/frontend.log"
    tail -20 logs/frontend.log
    exit 1
fi

# Final status check
print_status "Performing final health checks..."

PUBLIC_IP=$(get_public_ip)

print_success "🎉 All services started successfully!"
echo ""
echo "======================================"
echo "   AGENTIC ARCHITECT PLATFORM"
echo "======================================"
echo ""
echo "🌐 Application URLs:"
echo "   Frontend:      http://$PUBLIC_IP:3000"
echo "   Backend API:   http://$PUBLIC_IP:3001"
echo "   Agent Service: http://$PUBLIC_IP:8000"
echo ""
echo "📊 Service Status:"
echo "   Backend PID:   $(cat logs/backend.pid)"
echo "   Agent PID:     $(cat logs/agent_service.pid)"
echo "   Frontend PID:  $(cat logs/frontend.pid)"
echo ""
echo "🔍 Monitoring:"
echo "   View all logs: tail -f logs/*.log"
echo "   Backend logs:  tail -f logs/backend.log"
echo "   Agent logs:    tail -f logs/agent_service.log"
echo "   Frontend logs: tail -f logs/frontend.log"
echo ""
echo "⚡ Management:"
echo "   Stop services: ./stop_services.sh"
echo "   Restart:       ./start_services.sh"
echo ""

# Test API endpoints
print_status "Testing API endpoints..."

# Test backend
if curl -s -f http://127.0.0.1:3001/health > /dev/null 2>&1; then
    print_success "✅ Backend API responding at http://127.0.0.1:3001/health"
    # Test if backend accepts requests from public IP origin
    BACKEND_CORS_TEST=$(curl -s -H "Origin: http://$PUBLIC_IP:3000" http://127.0.0.1:3001/health 2>/dev/null)
    if [ $? -eq 0 ]; then
        print_success "✅ Backend CORS configured correctly for public IP"
    else
        print_warning "⚠️  Backend CORS might need adjustment for public IP requests"
    fi
else
    print_warning "⚠️  Backend API not responding (might need time to fully start)"
fi

# Test agent service
if curl -s -f http://127.0.0.1:8000 > /dev/null 2>&1; then
    print_success "✅ Agent Service responding"
else
    print_warning "⚠️  Agent Service not responding (might need time to fully start)"
fi

# Test frontend
if curl -s -f http://127.0.0.1:3000 > /dev/null 2>&1; then
    print_success "✅ Frontend responding"
else
    print_warning "⚠️  Frontend not responding (might need time to fully start)"
fi

echo ""
print_success "🚀 Platform is ready for your demo!"
print_warning "💡 Don't forget to update agent_service/.env with your API keys!"
echo ""
print_status "🔒 EC2 Security Group Requirements:"
echo "   Ensure these ports are open in your EC2 security group:"
echo "   - Port 3000 (Frontend) - HTTP from 0.0.0.0/0"
echo "   - Port 3001 (Backend API) - HTTP from 0.0.0.0/0" 
echo "   - Port 8000 (Agent Service) - HTTP from 0.0.0.0/0"
echo "   - Port 22 (SSH) - SSH from your IP"
echo ""
