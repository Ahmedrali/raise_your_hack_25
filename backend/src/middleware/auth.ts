import { Request, Response, NextFunction } from 'express';
import { UserProfile } from '../types/api';
import { SimpleAuthService } from '../services/simple-auth.service';
import PrismaService from '../services/prisma.service';

export interface AuthenticatedRequest extends Request {
  user?: UserProfile;
  prisma?: any;
}

export async function authMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'No valid authorization token provided'
        }
      });
      return;
    }

    const token = authHeader.substring(7); // Remove 'Bearer ' prefix
    
    try {
      const prisma = PrismaService.getInstance();
      const authService = new SimpleAuthService(prisma);
      const user = await authService.validateToken(token);
      
      if (!user) {
        res.status(401).json({
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: 'Invalid or expired token'
          }
        });
        return;
      }

      req.user = user;
      next();
    } catch (authError) {
      res.status(401).json({
        success: false,
        error: {
          code: 'INVALID_TOKEN',
          message: 'Invalid or expired token'
        }
      });
      return;
    }
  } catch (error) {
    console.error('Auth middleware error:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'AUTH_ERROR',
        message: 'Authentication error occurred'
      }
    });
  }
}
