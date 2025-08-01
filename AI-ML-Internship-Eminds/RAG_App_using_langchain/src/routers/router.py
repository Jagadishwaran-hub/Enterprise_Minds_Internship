from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List
import sys
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pdf_service import PDFService
from services.vector_service import VectorService
from services.llm_service import LLMService

class LangChainRAGAPIRouter:
    def __init__(self, app: Flask = None):
        """Initialize the LangChain RAG API Router"""
        self.app = app
        self.pdf_service = None
        self.vector_service = None
        self.llm_service = None
        self.initialized = False
        self.pdf_processed = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize the router with Flask app"""
        self.app = app
        self._register_routes()
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize PDF, Vector, and LLM services"""
        try:
            print("Initializing LangChain RAG services...")
            self.pdf_service = PDFService()
            self.vector_service = VectorService()
            self.llm_service = LLMService()
            self.initialized = True
            print("LangChain RAG services initialized successfully!")
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
                        "pdf_service": self.pdf_service is not None,
                        "vector_service": self.vector_service is not None,
                        "llm_service": self.llm_service is not None
                    },
                    "pdf_processed": self.pdf_processed,
                    "timestamp": str(Path().cwd())
                }
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"status": "unhealthy", "error": str(e)}), 500
        
        # Test endpoint for debugging
        @self.app.route('/test', methods=['GET'])
        def test_endpoint():
            """Test endpoint for debugging"""
            return jsonify({
                "message": "API is working!",
                "endpoints": {
                    "health": "/health",
                    "docs": "/docs or /api/docs",
                    "query": "/api/query or /query (GET/POST)",
                    "upload_text": "/api/documents/text (POST)",
                    "status": "/api/status (GET)"
                },
                "usage_examples": {
                    "get_query": "GET /api/query?question=What is AI?",
                    "post_query": "POST /api/query with JSON body",
                    "get_docs": "GET /docs or GET /api/docs"
                }
            })
        
        # Info endpoint with current status and helpful tips
        @self.app.route('/info', methods=['GET'])
        def info_endpoint():
            """Info endpoint with current status and helpful tips"""
            return jsonify({
                "message": "LangChain RAG API Status",
                "current_status": {
                    "services_initialized": self.initialized,
                    "pdf_processed": self.pdf_processed,
                    "ready_for_queries": self.initialized and self.pdf_processed
                },
                "quick_actions": {
                    "check_health": "GET /health",
                    "view_docs": "GET /docs",
                    "upload_text": "POST /api/documents/text",
                    "query": "GET /api/query?question=Your question"
                },
                "next_steps": [
                    "1. Check health: curl http://localhost:5000/health",
                    "2. Upload text: curl -X POST http://localhost:5000/api/documents/text -H \"Content-Type: application/json\" -d '{\"text\": \"Your text here\"}'",
                    "3. Query: curl \"http://localhost:5000/api/query?question=What is AI?\""
                ] if self.initialized and not self.pdf_processed else [
                    "1. Check health: curl http://localhost:5000/health",
                    "2. Query: curl \"http://localhost:5000/api/query?question=What is AI?\""
                ] if self.initialized and self.pdf_processed else [
                    "1. Wait for services to initialize",
                    "2. Check health: curl http://localhost:5000/health"
                ]
            })
        
        # System status endpoint
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get system status and information"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                # Get vector store info
                vector_info = self.vector_service.get_vector_store_info()
                
                # Get LLM info
                llm_info = self.llm_service.get_model_info()
                
                status = {
                    "pdf_processed": self.pdf_processed,
                    "vector_store": vector_info,
                    "llm_service": llm_info,
                    "services_initialized": self.initialized
                }
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # PDF upload and processing endpoint
        @self.app.route('/api/documents/upload', methods=['POST'])
        def upload_pdf():
            """Upload and process PDF documents"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                # Check if file is present
                if 'file' not in request.files:
                    return jsonify({"error": "No file provided"}), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                
                # Check file type
                filename = secure_filename(file.filename)
                if not filename.lower().endswith('.pdf'):
                    return jsonify({"error": "Only PDF files are supported"}), 400
                
                # Get additional parameters
                chunk_size = request.form.get('chunk_size', 1000, type=int)
                chunk_overlap = request.form.get('chunk_overlap', 200, type=int)
                model_name = request.form.get('model_name', 'llama3-8b-8192')
                
                # Save uploaded file
                temp_path = self.pdf_service.save_uploaded_file(file)
                
                # Extract text from PDF
                raw_text = self.pdf_service.extract_text_from_pdf(temp_path)
                
                # Split text into chunks
                text_chunks = self.pdf_service.get_text_chunks(raw_text, chunk_size, chunk_overlap)
                
                # Create vector store
                vector_store = self.vector_service.create_vector_store(text_chunks)
                
                # Initialize LLM service with selected model
                self.llm_service = LLMService(model_name=model_name)
                
                # Save vector store
                save_path = self.vector_service.save_vector_store()
                
                # Cleanup temp file
                self.pdf_service.cleanup_temp_file(temp_path)
                
                # Update status
                self.pdf_processed = True
                
                return jsonify({
                    "message": "PDF processed successfully",
                    "filename": filename,
                    "text_chunks_created": len(text_chunks),
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "model_name": model_name,
                    "vector_store_saved": save_path
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
                chunk_size = data.get('chunk_size', 1000)
                chunk_overlap = data.get('chunk_overlap', 200)
                model_name = data.get('model_name', 'llama3-8b-8192')
                
                # Split text into chunks
                text_chunks = self.pdf_service.get_text_chunks(text_content, chunk_size, chunk_overlap)
                
                # Create vector store
                vector_store = self.vector_service.create_vector_store(text_chunks)
                
                # Initialize LLM service with selected model
                self.llm_service = LLMService(model_name=model_name)
                
                # Save vector store
                save_path = self.vector_service.save_vector_store()
                
                # Update status
                self.pdf_processed = True
                
                return jsonify({
                    "message": "Text processed successfully",
                    "source_name": source_name,
                    "text_chunks_created": len(text_chunks),
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "model_name": model_name,
                    "vector_store_saved": save_path
                }), 200
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Query endpoint (with /api prefix) - supports both GET and POST
        @self.app.route('/api/query', methods=['GET', 'POST'])
        def query():
            """Query the RAG system"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                # Handle both GET and POST requests
                if request.method == 'GET':
                    # For GET requests, get parameters from query string
                    question = request.args.get('question')
                    k_results = request.args.get('k_results', 4, type=int)
                else:
                    # For POST requests, try to get data from JSON body first, then query params
                    data = request.get_json()
                    if data and 'question' in data:
                        # JSON body has the data
                        question = data['question']
                        k_results = data.get('k_results', 4)
                    else:
                        # Try to get from query parameters (for mixed POST requests)
                        question = request.args.get('question')
                        k_results = request.args.get('k_results', 4, type=int)
                        
                        if not question:
                            return jsonify({
                                "error": "No question provided in POST request",
                                "usage": {
                                    "post_with_json": "POST /api/query with JSON body: {\"question\": \"Your question here\"}",
                                    "post_with_params": "POST /api/query?question=Your question here",
                                    "get_with_params": "GET /api/query?question=Your question here"
                                },
                                "example": "Try: POST /api/query with JSON body {\"question\": \"What is AI?\"}"
                            }), 400
                
                if not question:
                    return jsonify({
                        "error": "No question provided",
                        "usage": {
                            "get": "GET /api/query?question=Your question here",
                            "post": "POST /api/query with JSON body: {\"question\": \"Your question here\"}"
                        },
                        "example": "Try: GET /api/query?question=What is artificial intelligence?"
                    }), 400
                
                if not self.pdf_processed:
                    return jsonify({
                        "error": "No documents processed. Please upload a PDF or text first.",
                        "next_steps": [
                            "Upload text: POST /api/documents/text with JSON body",
                            "Upload PDF: POST /api/documents/upload with file",
                            "Example: curl -X POST http://localhost:5000/api/documents/text -H \"Content-Type: application/json\" -d '{\"text\": \"Your text content here\"}'"
                        ]
                    }), 400
                
                # Perform similarity search
                docs = self.vector_service.similarity_search(question, k_results)
                
                # Get LLM response
                response = self.llm_service.get_response(docs, question)
                
                # Get model info
                model_info = self.llm_service.get_model_info()
                
                return jsonify({
                    "question": question,
                    "answer": response,
                    "k_results": k_results,
                    "model_info": model_info,
                    "documents_retrieved": len(docs)
                }), 200
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                return jsonify({
                    "error": f"Internal server error: {str(e)}",
                    "details": error_details if self.app.debug else "Enable debug mode for details"
                }), 500
        
        # Query endpoint (without /api prefix for convenience) - supports both GET and POST
        @self.app.route('/query', methods=['GET', 'POST'])
        def query_simple():
            """Query the RAG system (convenience endpoint)"""
            return query()
        
        # Documentation endpoint
        @self.app.route('/docs', methods=['GET'])
        def api_docs():
            """API Documentation endpoint"""
            return self._get_api_documentation()
        
        # API Documentation endpoint (with /api prefix)
        @self.app.route('/api/docs', methods=['GET'])
        def api_docs_with_prefix():
            """API Documentation endpoint (with /api prefix)"""
            return self._get_api_documentation()
    
    def _get_api_documentation(self):
        """Get API documentation"""
        return jsonify({
            "title": "LangChain RAG PDF Chatbot API Documentation",
            "version": "1.0.0",
            "description": "A comprehensive API for RAG-based PDF processing and querying using LangChain and Groq",
            "base_url": "/",
            "endpoints": {
                "health": {
                    "url": "/health",
                    "method": "GET",
                    "description": "Check system health and service status",
                    "response": {
                        "status": "healthy",
                        "services": "Object with service status",
                        "pdf_processed": "Boolean indicating if PDF is processed"
                    }
                },
                "docs": {
                    "url": "/docs",
                    "method": "GET", 
                    "description": "Get API documentation (this endpoint)",
                    "response": "Complete API documentation"
                },
                "status": {
                    "url": "/api/status",
                    "method": "GET",
                    "description": "Get detailed system status and information",
                    "response": {
                        "pdf_processed": "Boolean",
                        "vector_store": "Vector store information",
                        "llm_service": "LLM service information"
                    }
                },
                "upload_pdf": {
                    "url": "/api/documents/upload",
                    "method": "POST",
                    "description": "Upload and process PDF documents",
                    "content_type": "multipart/form-data",
                    "parameters": {
                        "file": "PDF file (required)",
                        "chunk_size": "Integer (default: 1000)",
                        "chunk_overlap": "Integer (default: 200)",
                        "model_name": "String (default: llama3-8b-8192)"
                    },
                    "response": {
                        "message": "Success message",
                        "filename": "Processed filename",
                        "text_chunks_created": "Number of chunks created"
                    }
                },
                "upload_text": {
                    "url": "/api/documents/text",
                    "method": "POST",
                    "description": "Upload text content directly",
                    "content_type": "application/json",
                    "body": {
                        "text": "Text content (required)",
                        "source_name": "String (default: manual_input)",
                        "chunk_size": "Integer (default: 1000)",
                        "chunk_overlap": "Integer (default: 200)",
                        "model_name": "String (default: llama3-8b-8192)"
                    },
                    "response": {
                        "message": "Success message",
                        "source_name": "Source name",
                        "text_chunks_created": "Number of chunks created"
                    }
                },
                "query": {
                    "url": "/api/query or /query",
                    "method": "GET/POST",
                    "description": "Query the RAG system",
                    "content_type": "application/json (for POST) or query parameters (for GET)",
                    "body": {
                        "question": "Question text (required)",
                        "k_results": "Integer (default: 4)"
                    },
                    "response": {
                        "question": "Original question",
                        "answer": "AI-generated answer",
                        "k_results": "Number of results used",
                        "model_info": "Model information",
                        "documents_retrieved": "Number of documents retrieved"
                    }
                },
                "update_model": {
                    "url": "/api/model",
                    "method": "PUT",
                    "description": "Update the LLM model",
                    "content_type": "application/json",
                    "body": {
                        "model_name": "Model name (required)"
                    },
                    "supported_models": [
                        "llama3-8b-8192",
                        "mixtral-8x7b-32768",
                        "llama3-70b-8192"
                    ],
                    "response": {
                        "message": "Success message",
                        "new_model": "Updated model name",
                        "model_info": "Model information"
                    }
                },
                "config": {
                    "url": "/api/config",
                    "method": "GET/PUT",
                    "description": "Get or update system configuration",
                    "get_response": {
                        "pdf_processed": "Boolean",
                        "model_info": "Model information",
                        "vector_store_info": "Vector store information",
                        "available_models": "List of available models"
                    },
                    "put_body": {
                        "model_name": "Model name to update"
                    }
                },
                "clear_documents": {
                    "url": "/api/documents",
                    "method": "DELETE",
                    "description": "Clear all documents and reset the system",
                    "response": {
                        "message": "Success message",
                        "system_reset": "Boolean"
                    }
                }
            },
            "examples": {
                "upload_text": {
                    "curl": 'curl -X POST http://localhost:5000/api/documents/text -H "Content-Type: application/json" -d \'{"text": "Your text here", "source_name": "test"}\'',
                    "python": '''
import requests
response = requests.post('http://localhost:5000/api/documents/text', 
                        json={'text': 'Your text here', 'source_name': 'test'})
print(response.json())
'''
                },
                "query": {
                    "curl_get": 'curl "http://localhost:5000/api/query?question=What is AI?"',
                    "curl_post": 'curl -X POST http://localhost:5000/api/query -H "Content-Type: application/json" -d \'{"question": "What is AI?", "k_results": 4}\'',
                    "python": '''
import requests
# GET request
response = requests.get('http://localhost:5000/api/query', params={'question': 'What is AI?'})
print(response.json())

# POST request
response = requests.post('http://localhost:5000/api/query', 
                        json={'question': 'What is AI?', 'k_results': 4})
print(response.json())
'''
                }
            },
            "error_codes": {
                "400": "Bad Request - Invalid input data",
                "404": "Not Found - Endpoint not found",
                "405": "Method Not Allowed - Wrong HTTP method",
                "500": "Internal Server Error - Server error",
                "503": "Service Unavailable - Services not initialized"
            }
        })
        
        # Model update endpoint
        @self.app.route('/api/model', methods=['PUT'])
        def update_model():
            """Update the LLM model"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                data = request.get_json()
                if not data or 'model_name' not in data:
                    return jsonify({"error": "No model name provided"}), 400
                
                model_name = data['model_name']
                valid_models = ["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]
                
                if model_name not in valid_models:
                    return jsonify({"error": f"Invalid model. Choose from: {valid_models}"}), 400
                
                # Update model
                self.llm_service.update_model(model_name)
                
                return jsonify({
                    "message": "Model updated successfully",
                    "new_model": model_name,
                    "model_info": self.llm_service.get_model_info()
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
                        "pdf_processed": self.pdf_processed,
                        "model_info": self.llm_service.get_model_info(),
                        "vector_store_info": self.vector_service.get_vector_store_info(),
                        "available_models": ["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]
                    }
                    return jsonify(config), 200
                
                elif request.method == 'PUT':
                    # Update configuration
                    data = request.get_json()
                    if not data:
                        return jsonify({"error": "No configuration data provided"}), 400
                    
                    # Update model if provided
                    if 'model_name' in data:
                        valid_models = ["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]
                        if data['model_name'] in valid_models:
                            self.llm_service.update_model(data['model_name'])
                    
                    return jsonify({
                        "message": "Configuration updated successfully",
                        "current_config": {
                            "pdf_processed": self.pdf_processed,
                            "model_info": self.llm_service.get_model_info(),
                            "vector_store_info": self.vector_service.get_vector_store_info()
                        }
                    }), 200
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Clear documents endpoint
        @self.app.route('/api/documents', methods=['DELETE'])
        def clear_documents():
            """Clear all documents and reset the system"""
            try:
                if not self.initialized:
                    return jsonify({"error": "Services not initialized"}), 503
                
                # Reset vector service
                self.vector_service = VectorService()
                
                # Reset LLM service
                self.llm_service = LLMService()
                
                # Update status
                self.pdf_processed = False
                
                return jsonify({
                    "message": "All documents cleared successfully",
                    "system_reset": True
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
def create_langchain_rag_router(app: Flask = None) -> LangChainRAGAPIRouter:
    """Create and return a LangChain RAG API Router instance"""
    return LangChainRAGAPIRouter(app)
