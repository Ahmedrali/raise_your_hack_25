# 🚀 Agentic Architect Platform

An intelligent multi-agent system for architectural design and business analysis, featuring AI-powered conversation flows and educational content generation.

## 🏗️ Architecture Overview

This platform consists of three interconnected services:

```
Frontend (React) :3000
    ↓
Backend (Node.js/TypeScript) :3001 ← PostgreSQL Database
    ↓
Agent Service (Python/FastAPI) :8000
```

## 🔧 Services

### 🤖 Agent Service (Python/FastAPI)
- **Location**: `./agent_service/`
- **Port**: 8000
- **Purpose**: AI-powered agents for architecture analysis, requirements gathering, and educational content
- **Key Features**:
  - Multi-agent orchestration
  - Groq LLM integration
  - Tavily search capabilities
  - Sequential workflow processing

### 🔐 Backend (Node.js/TypeScript)
- **Location**: `./backend/`
- **Port**: 3001
- **Purpose**: Authentication, user management, and data persistence
- **Key Features**:
  - JWT-based authentication
  - Prisma ORM with PostgreSQL
  - User session management
  - Conversation history storage

### 🎨 Frontend (React)
- **Location**: `./frontend/`
- **Port**: 3000
- **Purpose**: User interface and experience
- **Key Features**:
  - Modern React application
  - Real-time chat interface
  - Document upload capabilities
  - Responsive design

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Git

### One-Click Deployment (EC2)
```bash
git clone https://github.com/yourusername/raise_your_hack.git
cd raise_your_hack
chmod +x deploy.sh
./deploy.sh
```

### Local Development
```bash
# 1. Setup Backend
cd backend
npm install
npm run db:generate
npm run db:push
npm run dev

# 2. Setup Agent Service
cd agent_service
pip install -r requirements.txt
python main.py

# 3. Setup Frontend
cd frontend
npm install
npm start
```

## 🔑 Environment Configuration

### Backend (.env)
```bash
DATABASE_URL="postgresql://username:password@localhost:5432/agentic_architect_db"
JWT_SECRET="your-secret-key"
AGENT_SERVICE_URL="http://localhost:8000"
CORS_ORIGIN="http://localhost:3000"
```

### Agent Service (.env)
```bash
GROQ_API_KEY="your-groq-api-key"
TAVILY_API_KEY="your-tavily-api-key"
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:3001"
```

### Frontend (.env)
```bash
REACT_APP_API_URL="http://localhost:3001"
REACT_APP_AGENT_SERVICE_URL="http://localhost:8000"
```

## 🎯 Use Cases

1. **E-commerce Platform Architecture**
   - Requirements gathering and analysis
   - System design recommendations
   - Technology stack suggestions

2. **Educational Content Generation**
   - Interactive learning modules
   - Architecture explanations
   - Best practices documentation

3. **Business Impact Analysis**
   - Cost-benefit analysis
   - Risk assessment
   - Implementation roadmaps

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Agentic Architect Hackathon**
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL
- Redis
- Groq API key
- Tavily API key

### 1. Clone Repository
```bash
git clone <repository-url>
cd raise_your_hack
```

### 2. Start Agent Service
```bash
cd agent_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your API keys
echo "GROQ_API_KEY=your-groq-api-key" > .env
echo "TAVILY_API_KEY=your-tavily-api-key" >> .env

# Start Redis
redis-server

# Start agent service
python main.py
```

### 3. Start Backend
```bash
cd backend
npm install

# Create .env file
echo "DATABASE_URL=postgresql://username:password@localhost:5432/agentic_architect" > .env
echo "JWT_SECRET=your-super-secret-jwt-key" >> .env
echo "AGENT_SERVICE_URL=http://localhost:8000" >> .env

# Setup database
npm run db:generate
npm run db:push

# Start backend
npm run dev
```

### 4. Start Frontend
```bash
cd frontend
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:3001/api" > .env

# Start frontend
npm start
```

### 5. Access Application
Open your browser and navigate to `http://localhost:3000`

## 📁 Project Structure

```
raise_your_hack/
├── agent_service/          # Python AI agent service
│   ├── src/
│   │   ├── agents/         # Specialized AI agents
│   │   ├── api/            # FastAPI endpoints
│   │   ├── config/         # Configuration management
│   │   ├── models/         # Data models
│   │   ├── services/       # External service integrations
│   │   └── workflows/      # Agent orchestration
│   ├── tests/              # Test suite
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Agent service documentation
│
├── backend/               # Node.js backend service
│   ├── src/
│   │   ├── routes/        # API routes
│   │   ├── services/      # Business logic
│   │   ├── middleware/    # Express middleware
│   │   ├── types/         # TypeScript types
│   │   └── config/        # Configuration
│   ├── prisma/            # Database schema and migrations
│   ├── tests/             # Test suite
│   ├── package.json       # Node.js dependencies
│   └── README.md         # Backend documentation
│
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API integration
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   ├── public/            # Static assets
│   ├── package.json       # React dependencies
│   └── README.md         # Frontend documentation
│
├── requirements/          # Project requirements and documentation
└── README.md             # This file
```

## 🤖 AI Agents

The platform uses 7 specialized AI agents orchestrated through LangGraph:

1. **Requirements Agent** - Analyzes user requirements and constraints
2. **Architecture Agent** - Designs system architecture and selects technologies
3. **Research Agent** - Conducts technology research and gathers best practices
4. **Business Impact Agent** - Assesses business implications and ROI
5. **Educational Agent** - Provides learning content and explanations
6. **Documentation Agent** - Generates technical documentation
7. **Why Reasoning Agent** - Explains decision rationale and context

## 🛠️ Technology Stack

### Frontend
- **React 19.1.0** - UI framework
- **TypeScript** - Type safety
- **Styled Components** - CSS-in-JS styling
- **D3.js & Mermaid** - Data visualization
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Backend
- **Node.js** - Runtime environment
- **Express.js 4.21.2** - Web framework
- **TypeScript 5.7.3** - Type safety
- **Prisma 6.11.1** - Database ORM
- **PostgreSQL** - Primary database
- **JWT** - Authentication
- **Zod** - Runtime validation

### Agent Service
- **Python 3.11+** - Runtime environment
- **FastAPI 0.104.1** - Web framework
- **LangChain 0.0.340** - AI framework
- **LangGraph 0.0.40** - Agent orchestration
- **Groq 0.4.1** - LLM provider
- **Redis 5.0.1** - Caching and sessions
- **Tavily** - Web search integration

## 🔧 Configuration

### Environment Variables

Each service requires specific environment variables. See individual README files for detailed configuration:

- [Agent Service Configuration](agent_service/README.md#configuration)
- [Backend Configuration](backend/README.md#environment-configuration)
- [Frontend Configuration](frontend/README.md#environment-configuration)

### Port Configuration

Default ports:
- Frontend: 3000
- Backend: 3001
- Agent Service: 8000

To run on different ports:
```bash
# Frontend
PORT=3003 npm start

# Backend
PORT=3002 npm run dev

# Agent Service
PORT=8001 python main.py
```

## 🧪 Testing

### Run All Tests
```bash
# Agent Service
cd agent_service && pytest

# Backend
cd backend && npm test

# Frontend
cd frontend && npm test
```

### Test Coverage
```bash
# Agent Service
cd agent_service && pytest --cov=src --cov-report=html

# Backend
cd backend && npm run test:coverage

# Frontend
cd frontend && npm test -- --coverage --watchAll=false
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- Agent Service: `GET http://localhost:8000/health`
- Backend: `GET http://localhost:3001/api/health`

### Metrics
- Agent Service: `GET http://localhost:8000/metrics` (Prometheus format)

### Logs
All services provide structured logging for debugging and monitoring.

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's running on ports
   lsof -i :3000
   lsof -i :3001
   lsof -i :8000
   
   # Kill processes if needed
   kill -9 <PID>
   ```

2. **Database Connection Issues**
   ```bash
   # Check PostgreSQL is running
   pg_isready
   
   # Reset database
   cd backend && npm run db:push
   ```

3. **Redis Connection Issues**
   ```bash
   # Check Redis is running
   redis-cli ping
   
   # Start Redis
   redis-server
   ```

4. **API Key Issues**
   ```bash
   # Verify environment variables are set
   echo $GROQ_API_KEY
   echo $TAVILY_API_KEY
   ```

5. **Frontend API Connection**
   - Ensure backend is running on correct port
   - Check REACT_APP_API_URL in frontend/.env
   - Verify CORS configuration in backend

### Service Dependencies

Start services in this order:
1. PostgreSQL database
2. Redis server
3. Agent Service (port 8000)
4. Backend (port 3001)
5. Frontend (port 3000)

## 🔄 Development Workflow

### Making Changes

1. **Agent Logic Changes**
   ```bash
   cd agent_service
   # Make changes to agents
   pytest  # Run tests
   python main.py  # Restart service
   ```

2. **Backend API Changes**
   ```bash
   cd backend
   # Make changes to routes/services
   npm test  # Run tests
   npm run dev  # Auto-restart with nodemon
   ```

3. **Frontend UI Changes**
   ```bash
   cd frontend
   # Make changes to components
   npm test  # Run tests
   # Hot reload automatically updates browser
   ```

### Code Quality

```bash
# Agent Service
cd agent_service
black src/  # Format code
isort src/  # Sort imports
mypy src/   # Type checking

# Backend
cd backend
npm run lint  # ESLint
npm run lint:fix  # Auto-fix issues

# Frontend
# ESLint runs automatically with Create React App
```

## 📚 Documentation

- [Agent Service Documentation](agent_service/README.md)
- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Requirements Documentation](requirements/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the troubleshooting sections in individual README files
2. Review the logs for error details
3. Ensure all prerequisites are installed and configured
4. Verify environment variables are set correctly
