#!/usr/bin/env python3
"""
LangChain RAG PDF Chatbot API Client Example

This script demonstrates how to use the LangChain RAG API endpoints
to upload PDFs, query the system, and manage configuration.
"""

import requests
import json
import os
from pathlib import Path

class LangChainRAGAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        """Initialize the API client"""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self):
        """Check API health"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_status(self):
        """Get system status"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def upload_pdf(self, file_path, chunk_size=1000, chunk_overlap=200, model_name="llama3-8b-8192"):
        """Upload and process a PDF file"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}, 404
            
            if not file_path.lower().endswith('.pdf'):
                return {"error": "Only PDF files are supported"}, 400
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'chunk_size': chunk_size,
                    'chunk_overlap': chunk_overlap,
                    'model_name': model_name
                }
                response = self.session.post(
                    f"{self.base_url}/api/documents/upload",
                    files=files,
                    data=data
                )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def upload_text(self, text, source_name="manual_input", chunk_size=1000, chunk_overlap=200, model_name="llama3-8b-8192"):
        """Upload text content directly"""
        try:
            data = {
                'text': text,
                'source_name': source_name,
                'chunk_size': chunk_size,
                'chunk_overlap': chunk_overlap,
                'model_name': model_name
            }
            response = self.session.post(
                f"{self.base_url}/api/documents/text",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def query(self, question, k_results=4):
        """Query the RAG system"""
        try:
            data = {
                'question': question,
                'k_results': k_results
            }
            response = self.session.post(
                f"{self.base_url}/api/query",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def update_model(self, model_name):
        """Update the LLM model"""
        try:
            data = {
                'model_name': model_name
            }
            response = self.session.put(
                f"{self.base_url}/api/model",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_config(self):
        """Get system configuration"""
        try:
            response = self.session.get(f"{self.base_url}/api/config")
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def clear_documents(self):
        """Clear all documents"""
        try:
            response = self.session.delete(f"{self.base_url}/api/documents")
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500

def main():
    """Example usage of the LangChain RAG API client"""
    
    # Initialize client
    client = LangChainRAGAPIClient()
    
    print("🤖 LangChain RAG PDF Chatbot API Client Example")
    print("=" * 60)
    
    # Health check
    print("\n1. Health Check:")
    health, status = client.health_check()
    print(f"Status: {status}")
    print(f"Response: {json.dumps(health, indent=2)}")
    
    if status != 200:
        print("❌ API is not healthy. Please check if the server is running.")
        return
    
    # Get system status
    print("\n2. System Status:")
    status_info, status_code = client.get_status()
    print(f"Status: {status_code}")
    print(f"Response: {json.dumps(status_info, indent=2)}")
    
    # Upload sample text
    print("\n3. Upload Sample Text:")
    sample_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create 
    intelligent machines that work and react like humans. Some of the activities 
    computers with artificial intelligence are designed for include speech recognition, 
    learning, planning, and problem solving. Machine learning is a subset of AI that 
    enables computers to learn and improve from experience without being explicitly programmed.
    """
    result, status = client.upload_text(
        sample_text, 
        "ai_introduction",
        chunk_size=1000,
        chunk_overlap=200,
        model_name="llama3-8b-8192"
    )
    print(f"Status: {status}")
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Query the system
    print("\n4. Query the System:")
    question = "What is artificial intelligence and how does it relate to machine learning?"
    result, status = client.query(question, k_results=4)
    print(f"Status: {status}")
    print(f"Question: {question}")
    print(f"Answer: {result.get('answer', 'No answer')}")
    print(f"Model: {result.get('model_info', {}).get('model_name', 'N/A')}")
    print(f"Documents Retrieved: {result.get('documents_retrieved', 'N/A')}")
    
    # Get configuration
    print("\n5. Current Configuration:")
    config, status = client.get_config()
    print(f"Status: {status}")
    print(f"Response: {json.dumps(config, indent=2)}")
    
    # Update model
    print("\n6. Update Model:")
    result, status = client.update_model("mixtral-8x7b-32768")
    print(f"Status: {status}")
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Query with new model
    print("\n7. Query with Updated Model:")
    question2 = "What are the main applications of AI?"
    result, status = client.query(question2, k_results=3)
    print(f"Status: {status}")
    print(f"Question: {question2}")
    print(f"Answer: {result.get('answer', 'No answer')}")
    print(f"Model: {result.get('model_info', {}).get('model_name', 'N/A')}")
    
    print("\n✅ LangChain RAG API client example completed!")

if __name__ == "__main__":
    main() 