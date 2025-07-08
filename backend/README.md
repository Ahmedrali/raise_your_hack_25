# Agentic Architect Backend

Backend service for the Agentic Architect platform - an AI-powered architecture consulting system that provides expert guidance on system design with comprehensive explanations and business insights.

## Tech Stack

- **Runtime**: Node.js (v18+ recommended)
- **Language**: TypeScript 5.7.3
- **Framework**: Express.js 4.21.2
- **Database**: PostgreSQL with Prisma ORM 6.11.1
- **Authentication**: JWT with bcryptjs
- **Validation**: Zod 3.24.1
- **HTTP Client**: Axios 1.7.9
- **Security**: Helmet, CORS, Rate Limiting
- **Testing**: Jest 30.0.4 with Supertest
- **Development**: Nodemon, ts-node

## Prerequisites

- Node.js 18+ 
- npm or yarn
- PostgreSQL database
- Agent Service running on port 8000

## Installation

1. **Clone the repository and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```env
   # Database
   DATABASE_URL="postgresql://username:password@localhost:5432/agentic_architect"
   
   # JWT
   JWT_SECRET="your-super-secret-jwt-key-here"
   JWT_EXPIRES_IN="7d"
   
   # Agent Service
   AGENT_SERVICE_URL="http://localhost:8000"
   
   # Server
   PORT=3001
   NODE_ENV="development"
   
   # CORS
   FRONTEND_URL="http://localhost:3000"
   ```

4. **Set up the database**
   ```bash
   # Generate Prisma client
   npm run db:generate
   
   # Push database schema
   npm run db:push
   
   # Optional: Seed the database
   npm run db:seed
   ```

## Running the Application

### Development Mode
```bash
npm run dev
```
The server will start on `http://localhost:3001` with hot reloading enabled.

### Production Mode
```bash
# Build the application
npm run build

# Start the production server
npm start
```

### Alternative Port
To run on a different port (e.g., 3002):
```bash
PORT=3002 npm run dev
```

## Available Scripts

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build TypeScript to JavaScript
- `npm start` - Start production server
- `npm test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report
- `npm run db:generate` - Generate Prisma client
- `npm run db:push` - Push schema to database
- `npm run db:migrate` - Run database migrations
- `npm run db:seed` - Seed database with initial data
- `npm run db:studio` - Open Prisma Studio
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Conversations
- `POST /api/conversations` - Start new conversation
- `GET /api/conversations` - Get user conversations
- `GET /api/conversations/:id` - Get specific conversation
- `POST /api/conversations/:id/messages` - Send message

### Health Check
- `GET /api/health` - Service health status

## Database Schema

The application uses Prisma ORM with PostgreSQL. Key entities:
- **Users** - User accounts and profiles
- **Conversations** - Architecture consultation sessions
- **Messages** - Conversation messages and agent responses
- **Architecture Updates** - Generated architecture recommendations

## Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `JWT_EXPIRES_IN` | JWT token expiration | "7d" |
| `AGENT_SERVICE_URL` | Agent service endpoint | "http://localhost:8000" |
| `PORT` | Server port | 3001 |
| `NODE_ENV` | Environment mode | "development" |
| `FRONTEND_URL` | Frontend URL for CORS | "http://localhost:3000" |

## Testing

Run the test suite:
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Run `npm run db:push` to sync schema

2. **Agent Service Connection Error**
   - Ensure agent service is running on port 8000
   - Check AGENT_SERVICE_URL in .env file

3. **Port Already in Use**
   - Change PORT in .env file or use `PORT=3002 npm run dev`

4. **JWT Token Issues**
   - Ensure JWT_SECRET is set in .env file
   - Clear browser localStorage if needed

### Logs

The application logs important events including:
- Agent service requests and responses
- Authentication attempts
- Database operations
- Error details

Check the console output for detailed logging information.

## Development Notes

- The backend currently uses a mock conversation service for development
- Real agent service integration is available when agent service is running
- Authentication uses simple JWT tokens (enhance for production)
- Rate limiting is enabled for API protection
- CORS is configured for frontend integration
