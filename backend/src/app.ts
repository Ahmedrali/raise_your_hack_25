import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import { errorHandler, notFoundHandler } from './middleware/error-handling';
import { authMiddleware } from './middleware/auth';
import PrismaService from './services/prisma.service';

// Route imports
import authRoutes from './routes/auth';
import conversationRoutes from './routes/conversations';

const app = express();

// Security middleware
app.use(helmet());
const allowedOrigins = [ 
  'http://localhost:3000', 
  'http://localhost:3002',
  'http://54.194.104.191:3000',
  'http://54.194.104.191:3001',
  'http://54.194.104.191:8000'
];

app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    
    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      console.log(`CORS blocked request from origin: ${origin}`);
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

// Body parsing and compression
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check (before auth)
app.get('/health', async (req, res) => {
  const dbHealthy = await PrismaService.healthCheck();
  
  res.json({
    status: dbHealthy ? 'healthy' : 'degraded',
    service: 'agentic-architect-backend',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    database: dbHealthy ? 'connected' : 'disconnected'
  });
});

// Authentication routes (no auth required)
app.use('/api/auth', authRoutes);

// Protected routes
app.use('/api/conversations', authMiddleware, conversationRoutes);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

export default app;
