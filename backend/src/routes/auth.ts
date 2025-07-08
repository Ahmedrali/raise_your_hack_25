import { Router } from 'express';
import { z } from 'zod';
import { validationMiddleware } from '../middleware/validation';
import { SimpleAuthService } from '../services/simple-auth.service';
import PrismaService from '../services/prisma.service';

import { v4 as uuidv4 } from 'uuid';
import { ExpertiseLevel } from '../types/api';

const router = Router();

// Initialize Prisma client
const prisma = PrismaService.getInstance();

// Validation schemas
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  firstName: z.string().optional(),
  lastName: z.string().optional(),
  expertiseLevel: z.enum(['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']).optional(),
  businessRole: z.string().optional(),
  businessContext: z.object({
    industry: z.string().optional(),
    companySize: z.enum(['startup', 'small', 'medium', 'large', 'enterprise']).optional(),
    budgetRange: z.enum(['limited', 'moderate', 'significant', 'unlimited']).optional(),
    timeline: z.enum(['immediate', 'weeks', 'months', 'flexible']).optional()
  }).optional()
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
});

// Routes
router.post('/register', validationMiddleware(createUserSchema), async (req, res) => {
  try {
    const authService = new SimpleAuthService(prisma);
    const user = await authService.createUser(req.body);
    
    res.status(201).json({
      success: true,
      data: { user }
    });
  } catch (error: any) {
    console.error('Registration failed:', error);
    res.status(400).json({
      success: false,
      error: {
        code: 'REGISTRATION_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/login', validationMiddleware(loginSchema), async (req, res) => {
  try {
    const authService = new SimpleAuthService(prisma);
    const loginResult = await authService.login(req.body);
    
    res.json({
      success: true,
      data: loginResult
    });
  } catch (error: any) {
    console.error('Login failed:', error);
    res.status(401).json({
      success: false,
      error: {
        code: 'LOGIN_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/guest', async (req, res) => {
  try {
    const authService = new SimpleAuthService(prisma);
    const guestEmail = `guest-${uuidv4()}@example.com`;
    const guestPassword = uuidv4(); // random password

    const user = await authService.createUser({
      email: guestEmail,
      password: guestPassword,
      firstName: 'Guest',
      lastName: 'User',
      expertiseLevel: ExpertiseLevel.INTERMEDIATE
    });

    // Login the guest user to get token
    const loginResult = await authService.login({
      email: guestEmail,
      password: guestPassword
    });

    res.status(201).json({
      success: true,
      data: loginResult
    });
  } catch (error: any) {
    console.error('Guest user creation failed:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'GUEST_CREATION_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/logout', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      // Token invalidation would happen here
      // For now, just return success
    }
    
    res.json({
      success: true,
      message: 'Logged out successfully'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: {
        code: 'LOGOUT_ERROR',
        message: error.message
      }
    });
  }
});

export default router;
