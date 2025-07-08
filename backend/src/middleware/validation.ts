import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export function validationMiddleware(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Request validation failed',
            details: error.errors
          }
        });
      } else {
        next(error);
      }
    }
  };
}
