from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from pathlib import Path
import PyPDF2
from typing import Dict, Any, List
import sys
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.service1 import RAGService
from services.llm_service import LLMService

class RAGAPIRouter:
    def __init__(self, app: Flask = None):
        """Initialize the RAG API Router"""
        self.app = app
        self.rag_service = None
        self.llm_service = None
        self.initialized = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize the router with Flask app"""
        self.app = app
        self._register_routes()
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize RAG and LLM services"""
        try:
            print("Initializing RAG services...")
            self.rag_service = RAGService()
            self.rag_service.initialize()
            self.llm_service = LLMService()
            self.llm_service.initialize()
            self.initialized = True
            print("RAG services initialized successfully!")
        except Exception as e:
            print(f"Error initializing services: {e}")
            self.initialized = False
    
    def _register_routes(self):
        """Register all API routes"""
        
        # Health check endpoint
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            try:
                status = {
                    "status": "healthy",
                    "services": {
                        "rag_service": self.initialized,
                        "llm_service": self.llm_service is not None
                    },
                    "timestamp": str(Path().cwd())
                }
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"status": "unhealthy", "error": str(e)}), 500
        
        # System status endpoint
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get system status and information"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                status = self.rag_service.get_status()
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Document upload endpoint
        @self.app.route('/api/documents/upload', methods=['POST'])
        def upload_document():
            """Upload and process documents"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                # Check if file is present
                if 'file' not in request.files:
                    return jsonify({"error": "No file provided"}), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                
                # Get additional parameters
                chunk_size = request.form.get('chunk_size', 512, type=int)
                chunk_overlap = request.form.get('chunk_overlap', 50, type=int)
                
                # Update chunking settings
                self.rag_service.chunk_size = chunk_size
                self.rag_service.chunk_overlap = chunk_overlap
                
                # Process file based on type
                filename = secure_filename(file.filename)
                text_content = ""
                
                if filename.lower().endswith('.pdf'):
                    # Handle PDF files
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
                elif filename.lower().endswith('.txt'):
                    # Handle text files
                    text_content = file.read().decode('utf-8')
                else:
                    return jsonify({"error": "Unsupported file type. Use PDF or TXT files."}), 400
                
                # Add document to RAG service
                documents_added = self.rag_service.add_documents([text_content], [filename])
                
                return jsonify({
                    "message": "Document processed successfully",
                    "filename": filename,
                    "documents_added": documents_added,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap
                }), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Text upload endpoint
        @self.app.route('/api/documents/text', methods=['POST'])
        def upload_text():
            """Upload text content directly"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                data = request.get_json()
                if not data or 'text' not in data:
                    return jsonify({"error": "No text provided"}), 400
                
                text_content = data['text']
                source_name = data.get('source_name', 'manual_input')
                
                # Get chunking parameters
                chunk_size = data.get('chunk_size', 512)
                chunk_overlap = data.get('chunk_overlap', 50)
                
                # Update chunking settings
                self.rag_service.chunk_size = chunk_size
                self.rag_service.chunk_overlap = chunk_overlap
                
                # Add text to RAG service
                documents_added = self.rag_service.add_documents([text_content], [source_name])
                
                return jsonify({
                    "message": "Text processed successfully",
                    "source_name": source_name,
                    "documents_added": documents_added,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap
                }), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Query endpoint
        @self.app.route('/api/query', methods=['POST'])
        def query():
            """Query the RAG system"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                data = request.get_json()
                if not data or 'question' not in data:
                    return jsonify({"error": "No question provided"}), 400
                
                question = data['question']
                top_k = data.get('top_k', 3)
                
                # Perform query
                answer, sources, confidence = self.rag_service.query(question, top_k)
                
                return jsonify({
                    "question": question,
                    "answer": answer,
                    "sources": sources,
                    "confidence": confidence,
                    "top_k": top_k
                }), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Documents info endpoint
        @self.app.route('/api/documents', methods=['GET'])
        def get_documents():
            """Get information about stored documents"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                docs_info = self.rag_service.get_documents_info()
                return jsonify(docs_info), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Clear documents endpoint
        @self.app.route('/api/documents', methods=['DELETE'])
        def clear_documents():
            """Clear all documents from the system"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                self.rag_service.clear_documents()
                
                return jsonify({
                    "message": "All documents cleared successfully"
                }), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Configuration endpoint
        @self.app.route('/api/config', methods=['GET', 'PUT'])
        def config():
            """Get or update system configuration"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                if request.method == 'GET':
                    # Get current configuration
                    config = {
                        "chunk_size": self.rag_service.chunk_size,
                        "chunk_overlap": self.rag_service.chunk_overlap,
                        "embedding_model": self.rag_service.embedding_model_name,
                        "llm_model": self.llm_service.model_name
                    }
                    return jsonify(config), 200
                
                elif request.method == 'PUT':
                    # Update configuration
                    data = request.get_json()
                    if not data:
                        return jsonify({"error": "No configuration data provided"}), 400
                    
                    # Update chunking settings
                    if 'chunk_size' in data:
                        self.rag_service.chunk_size = data['chunk_size']
                    if 'chunk_overlap' in data:
                        self.rag_service.chunk_overlap = data['chunk_overlap']
                    
                    return jsonify({
                        "message": "Configuration updated successfully",
                        "config": {
                            "chunk_size": self.rag_service.chunk_size,
                            "chunk_overlap": self.rag_service.chunk_overlap,
                            "embedding_model": self.rag_service.embedding_model_name,
                            "llm_model": self.llm_service.model_name
                        }
                    }), 200
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500
        
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({"error": "Method not allowed"}), 405

# Factory function to create the router
def create_rag_router(app: Flask = None) -> RAGAPIRouter:
    """Create and return a RAG API Router instance"""
    return RAGAPIRouter(app) 