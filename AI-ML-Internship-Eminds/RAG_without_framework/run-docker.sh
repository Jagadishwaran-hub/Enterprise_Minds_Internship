#!/bin/bash

# RAG Frameworkless Docker Runner Script

echo "🚀 Starting RAG Frameworkless Application with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create necessary directories if they don't exist
mkdir -p data database logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating one from example..."
    cat > .env << EOF
# Groq API Configuration
# Get your API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Application Configuration
PYTHONPATH=/app
EOF
    echo "📝 Please edit .env file and add your Groq API key before running again."
    echo "🔑 Get your API key from: https://console.groq.com/"
    exit 1
fi

# Build and run with docker-compose
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting the application..."
docker-compose up -d

echo "✅ Application is starting up!"
echo "🌐 Access the application at: http://localhost:8502"
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop the application with: docker-compose down"
echo ""
echo "💡 Note: This app runs on port 8502 to avoid conflicts with other RAG apps" 