from flask import Flask, jsonify
from flask_cors import CORS
import os
from src.routers.router import create_langchain_rag_router

def create_app():
    """Create and configure the Flask application"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configure app settings
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = 'data'
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create and initialize LangChain RAG router
    rag_router = create_langchain_rag_router(app)
    
    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint with API information"""
        return jsonify({
            "message": "LangChain RAG PDF Chatbot API",
            "version": "1.0.0",
            "quick_start": {
                "health_check": "GET /health",
                "test": "GET /test",
                "api_docs": "GET /docs or GET /api/docs",
                "upload_text": "POST /api/documents/text",
                "query": "GET/POST /api/query or GET/POST /query"
            },
            "endpoints": {
                "health": "/health",
                "test": "/test",
                "docs": "/docs",
                "api_docs": "/api/docs",
                "status": "/api/status",
                "upload_pdf": "/api/documents/upload",
                "upload_text": "/api/documents/text",
                "query": "/api/query",
                "query_simple": "/query",
                "update_model": "/api/model",
                "config": "/api/config",
                "clear_documents": "/api/documents"
            },
            "documentation": {
                "health": "GET - Check system health",
                "docs": "GET - Get complete API documentation",
                "status": "GET - Get system status and information",
                "upload_pdf": "POST - Upload and process PDF files",
                "upload_text": "POST - Upload text content directly",
                "query": "POST - Query the RAG system (with /api prefix)",
                "query_simple": "POST - Query the RAG system (convenience endpoint)",
                "update_model": "PUT - Update LLM model",
                "config": "GET - Get configuration, PUT - Update configuration",
                "clear_documents": "DELETE - Clear all documents and reset system"
            },
            "supported_models": [
                "llama3-8b-8192",
                "mixtral-8x7b-32768", 
                "llama3-70b-8192"
            ],
            "example_usage": {
                "test": 'curl http://localhost:5000/test',
                "health": 'curl http://localhost:5000/health',
                "docs": 'curl http://localhost:5000/docs',
                "upload_text": 'curl -X POST http://localhost:5000/api/documents/text -H "Content-Type: application/json" -d \'{"text": "Your text here"}\'',
                "query_get": 'curl "http://localhost:5000/api/query?question=What is AI?"',
                "query_post": 'curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d \'{"question": "What is AI?"}\''
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting LangChain RAG PDF Chatbot API on port {port}")
    print(f"📖 API Documentation available at: http://localhost:{port}")
    print(f"🏥 Health check available at: http://localhost:{port}/health")
    print(f"🤖 Supported models: llama3-8b-8192, mixtral-8x7b-32768, llama3-70b-8192")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,  # Set to True for development and debugging
        threaded=True
    ) 