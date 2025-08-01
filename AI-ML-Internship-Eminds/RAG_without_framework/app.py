from flask import Flask, jsonify
from flask_cors import CORS
import os
from src.routers.router import create_rag_router

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
    
    # Create and initialize RAG router
    rag_router = create_rag_router(app)
    
    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint with API information"""
        return jsonify({
            "message": "RAG Frameworkless API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "status": "/api/status",
                "upload_document": "/api/documents/upload",
                "upload_text": "/api/documents/text",
                "query": "/api/query",
                "documents": "/api/documents",
                "config": "/api/config"
            },
            "documentation": {
                "health": "GET - Check system health",
                "status": "GET - Get system status and information",
                "upload_document": "POST - Upload PDF or TXT files",
                "upload_text": "POST - Upload text content directly",
                "query": "POST - Query the RAG system",
                "documents": "GET - Get document information, DELETE - Clear all documents",
                "config": "GET - Get configuration, PUT - Update configuration"
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting RAG Frameworkless API on port {port}")
    print(f"📖 API Documentation available at: http://localhost:{port}")
    print(f"🏥 Health check available at: http://localhost:{port}/health")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Set to True for development
        threaded=True
    ) 