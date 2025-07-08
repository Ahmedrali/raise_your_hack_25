import { PrismaClient } from '@prisma/client';

class PrismaService {
  private static instance: PrismaClient;

  static getInstance(): PrismaClient {
    if (!PrismaService.instance) {
      PrismaService.instance = new PrismaClient({
        log: process.env.NODE_ENV === 'development' ? ['query', 'info', 'warn', 'error'] : ['error'],
        errorFormat: 'pretty',
      });

      // Handle graceful shutdown
      process.on('beforeExit', async () => {
        await PrismaService.instance.$disconnect();
      });

      process.on('SIGINT', async () => {
        await PrismaService.instance.$disconnect();
        process.exit(0);
      });

      process.on('SIGTERM', async () => {
        await PrismaService.instance.$disconnect();
        process.exit(0);
      });
    }

    return PrismaService.instance;
  }

  static async disconnect(): Promise<void> {
    if (PrismaService.instance) {
      await PrismaService.instance.$disconnect();
    }
  }

  static async healthCheck(): Promise<boolean> {
    try {
      const prisma = PrismaService.getInstance();
      await prisma.$queryRaw`SELECT 1`;
      return true;
    } catch (error) {
      console.error('Database health check failed:', error);
      return false;
    }
  }
}

export default PrismaService;
