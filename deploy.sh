#!/bin/bash

# Agentic Architect Platform - EC2 Deployment Script
# This script deploys all three services on a single EC2 instance

set -e

echo "🚀 Starting Agentic Architect Platform Deployment..."

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
    curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "localhost"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root!"
    exit 1
fi

print_status "Installing system dependencies..."

# Update system
sudo yum update -y

# Install Node.js 18
print_status "Installing Node.js 18..."
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Python 3.11
print_status "Installing Python 3.11..."
sudo yum install -y python3 python3-pip python3-devel

# Install PostgreSQL 15
print_status "Installing PostgreSQL 15..."
sudo yum install -y postgresql15-server postgresql15
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Install other dependencies
sudo yum install -y git curl wget

print_success "System dependencies installed!"

# Setup PostgreSQL
print_status "Setting up PostgreSQL database..."

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE agentic_architect_db;
CREATE USER agentic_user WITH PASSWORD 'agentic_password_2025';
GRANT ALL PRIVILEGES ON DATABASE agentic_architect_db TO agentic_user;
ALTER USER agentic_user CREATEDB;
\q
EOF

print_success "PostgreSQL database created!"

# Setup environment files
print_status "Setting up environment files..."

# Backend environment
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    
    # Update database URL
    sed -i 's|DATABASE_URL=".*"|DATABASE_URL="postgresql://agentic_user:agentic_password_2025@localhost:5432/agentic_architect_db"|' backend/.env
    
    # Generate JWT secret
    JWT_SECRET=$(openssl rand -base64 32)
    sed -i "s|JWT_SECRET=\".*\"|JWT_SECRET=\"$JWT_SECRET\"|" backend/.env
    
    print_success "Backend environment configured!"
else
    print_warning "Backend .env already exists, skipping..."
fi

# Agent Service environment
if [ ! -f agent_service/.env ]; then
    cp agent_service/.env.example agent_service/.env
    print_warning "Please update agent_service/.env with your API keys!"
fi

# Frontend environment
if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    
    # Get public IP
    PUBLIC_IP=$(get_public_ip)
    
    # Update URLs for production
    sed -i "s|http://localhost:3001|http://$PUBLIC_IP:3001|" frontend/.env
    sed -i "s|http://localhost:8000|http://$PUBLIC_IP:8000|" frontend/.env
    
    print_success "Frontend environment configured!"
fi

# Install Backend Dependencies
print_status "Installing backend dependencies..."
cd backend
npm install

# Run Prisma migrations
print_status "Setting up database schema..."
npx prisma generate
npx prisma db push

cd ..

# Install Agent Service Dependencies
print_status "Installing agent service dependencies..."
cd agent_service
pip3 install -r requirements.txt
cd ..

# Install Frontend Dependencies
print_status "Installing frontend dependencies..."
cd frontend
npm install
cd ..

print_success "All dependencies installed!"

# Start services
print_status "Starting services..."

# Start Backend
print_status "Starting backend service..."
cd backend
npm run build
nohup npm start > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# Wait for backend to start
sleep 10

# Start Agent Service
print_status "Starting agent service..."
cd agent_service
nohup python3 main.py > ../logs/agent_service.log 2>&1 &
AGENT_PID=$!
echo $AGENT_PID > ../logs/agent_service.pid
cd ..

# Wait for agent service to start
sleep 10

# Start Frontend
print_status "Starting frontend service..."
cd frontend
nohup npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# Create logs directory
mkdir -p logs

# Wait for services to fully start
print_status "Waiting for services to start..."
sleep 30

# Check if services are running
print_status "Checking service status..."

# Check backend
if curl -f http://localhost:3001/api/health > /dev/null 2>&1; then
    print_success "Backend service is running!"
else
    print_warning "Backend service might not be ready yet..."
fi

# Check agent service
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Agent service is running!"
else
    print_warning "Agent service might not be ready yet..."
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend service is running!"
else
    print_warning "Frontend service might not be ready yet..."
fi

PUBLIC_IP=$(get_public_ip)

print_success "🎉 Deployment Complete!"
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
echo "🔍 Health Checks:"
echo "   Backend:   http://$PUBLIC_IP:3001/api/health"
echo "   Agent:     http://$PUBLIC_IP:8000/health"
echo ""
echo "📊 Monitoring:"
echo "   View logs: tail -f logs/*.log"
echo "   Stop services: ./stop_services.sh"
echo ""

# Create stop script
cat > stop_services.sh << 'EOF'
#!/bin/bash
echo "Stopping all services..."

if [ -f logs/frontend.pid ]; then
    kill $(cat logs/frontend.pid) 2>/dev/null
    rm logs/frontend.pid
    echo "Frontend stopped"
fi

if [ -f logs/backend.pid ]; then
    kill $(cat logs/backend.pid) 2>/dev/null
    rm logs/backend.pid
    echo "Backend stopped"
fi

if [ -f logs/agent_service.pid ]; then
    kill $(cat logs/agent_service.pid) 2>/dev/null
    rm logs/agent_service.pid
    echo "Agent service stopped"
fi

echo "All services stopped!"
EOF

chmod +x stop_services.sh

print_success "Deployment script completed!"
print_warning "Don't forget to update your API keys in agent_service/.env!"

echo ""
echo "Next steps:"
echo "1. Update agent_service/.env with your Groq and Tavily API keys"
echo "2. Test the application at http://$PUBLIC_IP:3000"
echo "3. Monitor logs with: tail -f logs/*.log"
