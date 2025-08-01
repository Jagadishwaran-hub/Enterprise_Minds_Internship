import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict, Any
import re
from pathlib import Path
import pickle
import shutil
from .llm_service import LLMService

class RAGService:
    def __init__(self):
        # Embedding model
        self.embedding_model = None
        self.embedding_model_name = "all-MiniLM-L6-v2"
        
        # FAISS index
        self.index = None
        self.documents = []
        self.document_embeddings = []
        
        # Chunking settings
        self.chunk_size = 512
        self.chunk_overlap = 50
        
        # Directories
        self.data_dir = Path("data")
        self.database_dir = Path("database")
        
        # Initialize LLM service
        self.llm_service = LLMService()
        
        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.database_dir.mkdir(exist_ok=True)
        
        # File paths
        self.index_file = self.database_dir / "faiss_index.bin"
        self.documents_file = self.database_dir / "documents.json"
        self.embeddings_file = self.database_dir / "embeddings.pkl"

    def initialize(self):
        """Initialize the RAG service"""
        try:
            # Load existing data
            self.load_existing_data()
            
            # Initialize LLM service
            self.llm_service.initialize()
            
            print("RAG service initialized successfully!")
        except Exception as e:
            print(f"Error initializing RAG service: {e}")
            raise

    def load_existing_data(self):
        """Load existing documents and index from disk"""
        try:
            if self.documents_file.exists():
                with open(self.documents_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                print(f"Loaded {len(self.documents)} existing documents")

            if self.index_file.exists() and self.embeddings_file.exists():
                # Load embeddings
                with open(self.embeddings_file, 'rb') as f:
                    self.document_embeddings = pickle.load(f)
                
                # Load FAISS index
                self.index = faiss.read_index(str(self.index_file))
                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                # Create new index
                self.index = None
                self.document_embeddings = []
        except Exception as e:
            print(f"Error loading existing data: {e}")
            self.documents = []
            self.document_embeddings = []
            self.index = None

    def save_data(self):
        """Save documents and index to disk"""
        try:
            # Save documents
            with open(self.documents_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            # Save embeddings
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.document_embeddings, f)
            
            # Save FAISS index
            if self.index is not None:
                faiss.write_index(self.index, str(self.index_file))
                
        except Exception as e:
            print(f"Error saving data: {e}")

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        return text.strip()

    def add_documents(self, texts: List[str], file_names: List[str] = None) -> int:
        """Add documents to the RAG system"""
        try:
            documents_added = 0
            
            for i, text in enumerate(texts):
                # Clean and chunk the text
                cleaned_text = self.clean_text(text)
                chunks = self.chunk_text(cleaned_text)
                
                # Get file name
                file_name = file_names[i] if file_names and i < len(file_names) else f"doc_{i}"
                
                # Save copy to data folder
                data_file_path = self.data_dir / f"{file_name}.txt"
                with open(data_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Add chunks as documents
                for j, chunk in enumerate(chunks):
                    doc_id = f"doc_{len(self.documents)}_{j}"
                    self.documents.append({
                        "id": doc_id,
                        "content": chunk,
                        "file_name": file_name,
                        "original_text": text[:100] + "..." if len(text) > 100 else text
                    })
                    documents_added += 1
            
            # Update embeddings and index
            self.update_embeddings()
            
            # Save to disk
            self.save_data()
            
            return documents_added
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            raise

    def update_embeddings(self):
        """Update embeddings for all documents"""
        try:
            if not self.documents:
                return
            
            # Load embedding model if not loaded
            if self.embedding_model is None:
                print("Loading embedding model...")
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Generate embeddings for all documents
            texts = [doc["content"] for doc in self.documents]
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            
            # Convert to float32 for FAISS
            embeddings = embeddings.astype(np.float32)
            self.document_embeddings = embeddings
            
            # Create or update FAISS index
            dimension = embeddings.shape[1]
            
            if self.index is None:
                # Create new index
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Clear existing vectors and add new ones
            self.index.reset()
            self.index.add(embeddings)
            
            print(f"Updated embeddings for {len(self.documents)} documents")
            
        except Exception as e:
            print(f"Error updating embeddings: {e}")
            raise

    def query(self, question: str, top_k: int = 3) -> Tuple[str, List[str], float]:
        """Query the RAG system"""
        try:
            if not self.documents or self.index is None:
                return "No documents available. Please upload some documents first.", [], 0.0
            
            # Load embedding model if not loaded
            if self.embedding_model is None:
                print("Loading embedding model...")
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Generate embedding for the question
            question_embedding = self.embedding_model.encode([question])
            question_embedding = question_embedding.astype(np.float32)
            
            # Search for similar documents
            scores, indices = self.index.search(question_embedding, top_k)
            
            # Get relevant documents
            relevant_docs = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents):
                    relevant_docs.append({
                        "content": self.documents[idx]["content"],
                        "score": float(score),
                        "id": self.documents[idx]["id"],
                        "file_name": self.documents[idx]["file_name"]
                    })
            
            # Generate answer using LLM
            answer = self.generate_answer_with_llm(question, relevant_docs)
            
            # Calculate confidence based on top score
            confidence = float(scores[0][0]) if scores[0].size > 0 else 0.0
            
            # Get source documents
            sources = [doc["id"] for doc in relevant_docs]
            
            return answer, sources, confidence
            
        except Exception as e:
            print(f"Error processing query: {e}")
            raise

    def generate_answer_with_llm(self, question: str, relevant_docs: List[Dict]) -> str:
        """Generate answer using LLM with retrieved documents"""
        if not relevant_docs:
            return "I don't have enough information to answer this question."
        
        # Prepare context from relevant documents
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        
        # Generate answer using LLM
        answer = self.llm_service.generate_answer(question, context)
        
        return answer

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the RAG service"""
        return {
            "documents_count": len(self.documents),
            "index_status": "ready" if self.index is not None else "not_ready",
            "embedding_model": self.embedding_model_name,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "llm_info": self.llm_service.get_model_info()
        }

    def get_documents_info(self) -> Dict[str, Any]:
        """Get information about stored documents"""
        return {
            "total_documents": len(self.documents),
            "documents": [
                {
                    "id": doc["id"],
                    "file_name": doc["file_name"],
                    "content_preview": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"],
                    "original_text_preview": doc["original_text"]
                }
                for doc in self.documents
            ]
        }

    def clear_documents(self):
        """Clear all documents from the system"""
        try:
            self.documents = []
            self.document_embeddings = []
            self.index = None
            
            # Remove saved files
            if self.documents_file.exists():
                self.documents_file.unlink()
            if self.embeddings_file.exists():
                self.embeddings_file.unlink()
            if self.index_file.exists():
                self.index_file.unlink()
            
            # Clear data folder
            if self.data_dir.exists():
                shutil.rmtree(self.data_dir)
                self.data_dir.mkdir(exist_ok=True)
            
            print("All documents cleared successfully")
            
        except Exception as e:
            print(f"Error clearing documents: {e}")
            raise
