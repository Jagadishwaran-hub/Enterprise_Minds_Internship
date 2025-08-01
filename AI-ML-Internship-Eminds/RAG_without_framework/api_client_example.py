#!/usr/bin/env python3
"""
RAG Frameworkless API Client Example

This script demonstrates how to use the RAG API endpoints
to upload documents, query the system, and manage configuration.
"""

import requests
import json
import os
from pathlib import Path

class RAGAPIClient:
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
    
    def upload_document(self, file_path, chunk_size=512, chunk_overlap=50):
        """Upload a document file"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}, 404
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'chunk_size': chunk_size,
                    'chunk_overlap': chunk_overlap
                }
                response = self.session.post(
                    f"{self.base_url}/api/documents/upload",
                    files=files,
                    data=data
                )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def upload_text(self, text, source_name="manual_input", chunk_size=512, chunk_overlap=50):
        """Upload text content directly"""
        try:
            data = {
                'text': text,
                'source_name': source_name,
                'chunk_size': chunk_size,
                'chunk_overlap': chunk_overlap
            }
            response = self.session.post(
                f"{self.base_url}/api/documents/text",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def query(self, question, top_k=3):
        """Query the RAG system"""
        try:
            data = {
                'question': question,
                'top_k': top_k
            }
            response = self.session.post(
                f"{self.base_url}/api/query",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_documents(self):
        """Get document information"""
        try:
            response = self.session.get(f"{self.base_url}/api/documents")
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
    
    def get_config(self):
        """Get system configuration"""
        try:
            response = self.session.get(f"{self.base_url}/api/config")
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def update_config(self, chunk_size=None, chunk_overlap=None):
        """Update system configuration"""
        try:
            data = {}
            if chunk_size is not None:
                data['chunk_size'] = chunk_size
            if chunk_overlap is not None:
                data['chunk_overlap'] = chunk_overlap
            
            response = self.session.put(
                f"{self.base_url}/api/config",
                json=data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500

def main():
    """Example usage of the RAG API client"""
    
    # Initialize client
    client = RAGAPIClient()
    
    print("🤖 RAG Frameworkless API Client Example")
    print("=" * 50)
    
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
    learning, planning, and problem solving.
    """
    result, status = client.upload_text(sample_text, "ai_introduction")
    print(f"Status: {status}")
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Query the system
    print("\n4. Query the System:")
    question = "What is artificial intelligence?"
    result, status = client.query(question, top_k=3)
    print(f"Status: {status}")
    print(f"Question: {question}")
    print(f"Answer: {result.get('answer', 'No answer')}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    
    # Get documents info
    print("\n5. Documents Information:")
    docs_info, status = client.get_documents()
    print(f"Status: {status}")
    print(f"Response: {json.dumps(docs_info, indent=2)}")
    
    # Get configuration
    print("\n6. Current Configuration:")
    config, status = client.get_config()
    print(f"Status: {status}")
    print(f"Response: {json.dumps(config, indent=2)}")
    
    print("\n✅ API client example completed!")

if __name__ == "__main__":
    main() 