#!/bin/bash

# Update the DATABASE_URL in the .env file
ENV_FILE=".env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file..."
    touch "$ENV_FILE"
fi

# Update or add DATABASE_URL
if grep -q "^DATABASE_URL=" "$ENV_FILE"; then
    # Replace existing DATABASE_URL
    sed -i '' 's|^DATABASE_URL=.*|DATABASE_URL="postgresql://ahmedali@localhost:5432/agentic_architect_db"|' "$ENV_FILE"
    echo "Updated DATABASE_URL in $ENV_FILE"
else
    # Add DATABASE_URL if it doesn't exist
    echo 'DATABASE_URL="postgresql://ahmedali@localhost:5432/agentic_architect_db"' >> "$ENV_FILE"
    echo "Added DATABASE_URL to $ENV_FILE"
fi

echo "Database configuration updated successfully!"
echo "You can now run: npm run dev"
