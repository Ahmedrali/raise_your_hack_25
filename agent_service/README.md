# Agentic Architect Agent Service

Python-based AI agent service for the Agentic Architect platform. This service orchestrates multiple specialized AI agents to provide comprehensive architecture consulting, including requirements analysis, system design, business impact assessment, and educational content delivery.

## Tech Stack

- **Runtime**: Python 3.11+
- **Framework**: FastAPI 0.104.1
- **ASGI Server**: Uvicorn 0.24.0
- **AI Framework**: LangChain 0.0.340 + LangGraph 0.0.40
- **LLM Provider**: Groq 0.4.1
- **Search**: Tavily Python 0.3.1
- **Cache**: Redis 5.0.1
- **Validation**: Pydantic 2.5.0
- **HTTP Client**: HTTPX 0.25.2
- **Logging**: Structlog 23.2.0
- **Monitoring**: Prometheus Client 0.19.0
- **Testing**: Pytest 7.4.3 with asyncio support
- **Code Quality**: Black, isort, mypy

## Prerequisites

- Python 3.11+
- pip or poetry
- Redis server (for caching)
- Groq API key
- Tavily API key (for research)

## Installation

1. **Clone the repository and navigate to agent service directory**
   ```bash
   cd agent_service
   ```

2. **Create and activate virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n agentic-architect python=3.11
   conda activate agentic-architect
   ```

3. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using pip with pyproject.toml
   pip install -e .
   ```

4. **Set up environment variables**
   Create a `.env` file in the agent_service directory:
   ```env
   # API Keys
   GROQ_API_KEY="your-groq-api-key-here"
   TAVILY_API_KEY="your-tavily-api-key-here"
   
   # Redis Configuration
   REDIS_URL="redis://localhost:6379"
   REDIS_PASSWORD=""
   
   # Service Configuration
   HOST="0.0.0.0"
   PORT=8000
   LOG_LEVEL="INFO"
   ENVIRONMENT="development"
   
   # Agent Configuration
   MAX_CONCURRENT_AGENTS=5
   AGENT_TIMEOUT=300
   CACHE_TTL=3600
   
   # LLM Configuration
   DEFAULT_MODEL="llama3-8b-8192"
   MAX_TOKENS=4096
   TEMPERATURE=0.7
   ```

5. **Start Redis server**
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:alpine
   
   # Or install locally and start
   redis-server
   ```

## Running the Application

### Development Mode
```bash
# Using uvicorn directly
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the main script
python main.py

# Or using the provided script
python -m src.api.main
```

### Production Mode
```bash
# Using uvicorn with production settings
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn (install separately)
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Alternative Port
```bash
PORT=8001 python main.py
```

## Available Scripts

### Development
```bash
# Start development server
python main.py

# Run with auto-reload
uvicorn src.api.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Production
```bash
# Start production server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Health check
curl http://localhost:8000/health
```

## Agent Architecture

### Specialized Agents

1. **Requirements Agent** (`requirements_agent.py`)
   - Analyzes user requirements
   - Extracts technical and business needs
   - Identifies constraints and priorities

2. **Architecture Agent** (`architecture_agent.py`)
   - Designs system architecture
   - Selects appropriate patterns and technologies
   - Creates scalable solutions

3. **Research Agent** (`research_agent.py`)
   - Conducts technology research
   - Gathers best practices
   - Provides market insights

4. **Business Impact Agent** (`business_impact_agent.py`)
   - Assesses business implications
   - Calculates ROI and costs
   - Identifies risks and opportunities

5. **Educational Agent** (`educational_agent.py`)
   - Provides learning content
   - Explains technical concepts
   - Offers implementation guidance

6. **Documentation Agent** (`documentation_agent.py`)
   - Generates technical documentation
   - Creates architecture diagrams
   - Produces implementation guides

7. **Why Reasoning Agent** (`why_reasoning_agent.py`)
   - Explains decision rationale
   - Provides context for recommendations
   - Justifies architectural choices

### Orchestrator

The **Orchestrator** (`orchestrator.py`) coordinates all agents using LangGraph to create a sequential workflow that ensures comprehensive analysis and recommendations.

## API Endpoints

### Core Endpoints
- `POST /api/agent/process` - Process conversation with agents
- `GET /health` - Service health check
- `GET /metrics` - Prometheus metrics

### Agent-Specific Endpoints
- `POST /api/agents/requirements` - Requirements analysis
- `POST /api/agents/architecture` - Architecture design
- `POST /api/agents/research` - Technology research
- `POST /api/agents/business-impact` - Business analysis
- `POST /api/agents/education` - Educational content
- `POST /api/agents/documentation` - Documentation generation

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | Required |
| `TAVILY_API_KEY` | Tavily API key for research | Required |
| `REDIS_URL` | Redis connection URL | "redis://localhost:6379" |
| `HOST` | Server host | "0.0.0.0" |
| `PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | "INFO" |
| `ENVIRONMENT` | Environment mode | "development" |
| `MAX_CONCURRENT_AGENTS` | Max concurrent agent executions | 5 |
| `AGENT_TIMEOUT` | Agent execution timeout (seconds) | 300 |
| `CACHE_TTL` | Cache time-to-live (seconds) | 3600 |
| `DEFAULT_MODEL` | Default LLM model | "llama3-8b-8192" |
| `MAX_TOKENS` | Maximum tokens per request | 4096 |
| `TEMPERATURE` | LLM temperature | 0.7 |

### Agent Configuration

Each agent can be configured through the settings system:

```python
# src/config/settings.py
class AgentSettings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str
    redis_url: str = "redis://localhost:6379"
    max_concurrent_agents: int = 5
    agent_timeout: int = 300
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_agents.py

# Run integration tests
pytest tests/integration/

# Run with verbose output
pytest -v
```

### Test Structure
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for workflows
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

## Monitoring

### Health Checks
```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health with dependencies
curl http://localhost:8000/health?detailed=true
```

### Metrics
Prometheus metrics are available at `/metrics`:
- Request counts and latencies
- Agent execution times
- Cache hit rates
- Error rates

### Logging
Structured logging with different levels:
- `DEBUG` - Detailed execution information
- `INFO` - General operational messages
- `WARNING` - Potential issues
- `ERROR` - Error conditions

## Troubleshooting

### Common Issues

1. **Groq API Key Error**
   ```bash
   # Check API key is set
   echo $GROQ_API_KEY
   
   # Test API connection
   curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
   ```

2. **Redis Connection Error**
   ```bash
   # Check Redis is running
   redis-cli ping
   
   # Check connection
   redis-cli -u $REDIS_URL ping
   ```

3. **Agent Timeout Issues**
   - Increase `AGENT_TIMEOUT` in environment
   - Check network connectivity
   - Monitor agent execution logs

4. **Memory Issues**
   - Reduce `MAX_CONCURRENT_AGENTS`
   - Implement request queuing
   - Monitor memory usage

### Performance Optimization

1. **Caching**
   - Enable Redis caching for repeated requests
   - Adjust `CACHE_TTL` based on use case

2. **Concurrency**
   - Tune `MAX_CONCURRENT_AGENTS` based on resources
   - Use async/await properly

3. **Model Selection**
   - Choose appropriate model for task complexity
   - Balance speed vs. quality

## Development Notes

- All agents inherit from `BaseAgent` for consistency
- LangGraph orchestrates agent workflows
- Redis provides caching and session management
- Structured logging enables debugging and monitoring
- Type hints and Pydantic ensure data validation
- Async/await patterns optimize performance
