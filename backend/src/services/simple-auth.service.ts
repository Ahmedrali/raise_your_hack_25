import { CreateUserRequest, LoginRequest, LoginResponse, UserProfile, ExpertiseLevel } from '../types/api';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export class SimpleAuthService {
  constructor(private prisma: any) {}

  async createUser(userData: CreateUserRequest): Promise<UserProfile> {
    // Check if user already exists
    const existingUser = await this.prisma.user.findUnique({
      where: { email: userData.email }
    });

    if (existingUser) {
      throw new Error('User with this email already exists');
    }

    // Hash password
    const passwordHash = await bcrypt.hash(userData.password, 10);

    // Create user in database
    const user = await this.prisma.user.create({
      data: {
        email: userData.email,
        password_hash: passwordHash,
        first_name: userData.firstName,
        last_name: userData.lastName,
        expertise_level: userData.expertiseLevel || ExpertiseLevel.INTERMEDIATE,
        business_role: userData.businessRole,
        business_context: userData.businessContext || {}
      }
    });

    return {
      id: user.id,
      email: user.email,
      firstName: user.first_name,
      lastName: user.last_name,
      expertiseLevel: user.expertise_level,
      businessRole: user.business_role,
      businessContext: user.business_context as any,
      createdAt: user.created_at
    };
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // Find user by email
    const user = await this.prisma.user.findUnique({
      where: { email: credentials.email }
    });

    if (!user) {
      throw new Error('Invalid email or password');
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(credentials.password, user.password_hash);
    if (!isValidPassword) {
      throw new Error('Invalid email or password');
    }

    // Update last login
    await this.prisma.user.update({
      where: { id: user.id },
      data: { last_login: new Date() }
    });

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: user.id, 
        email: user.email 
      },
      process.env.JWT_SECRET || 'your-super-secret-jwt-key',
      { expiresIn: '24h' }
    );

    const userProfile: UserProfile = {
      id: user.id,
      email: user.email,
      firstName: user.first_name,
      lastName: user.last_name,
      expertiseLevel: user.expertise_level,
      businessRole: user.business_role,
      businessContext: user.business_context as any,
      createdAt: user.created_at
    };

    return {
      user: userProfile,
      token,
      expiresIn: '24h'
    };
  }

  async validateToken(token: string): Promise<UserProfile | null> {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-super-secret-jwt-key') as any;
      
      const user = await this.prisma.user.findUnique({
        where: { id: decoded.userId }
      });

      if (!user) {
        return null;
      }

      return {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        expertiseLevel: user.expertise_level,
        businessRole: user.business_role,
        businessContext: user.business_context as any,
        createdAt: user.created_at
      };
    } catch (error) {
      return null;
    }
  }

  async logout(userId: string, token: string): Promise<void> {
    // For JWT tokens, we don't need to store them server-side
    // The client will simply discard the token
    console.log(`User ${userId} logged out`);
  }
}
