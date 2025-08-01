# RAG System with Groq & Llama 3-8B-8192

A clean Retrieval-Augmented Generation (RAG) system built with Streamlit and powered by Groq's Llama 3-8B-8192 model.

## Flow

1. **Query**: User asks a question
2. **Chunking**: Documents are split into chunks with overlap
3. **Embedding**: Text chunks are converted to vectors using Sentence Transformers
4. **FAISS Storage**: Vectors are stored in FAISS database for fast similarity search
5. **Retrieval**: Most relevant chunks are retrieved based on question similarity
6. **LLM Answer**: Groq's Llama 3-8B-8192 generates the final answer

## Features

- 📄 **Document Upload**: Upload text files and PDFs
- 🤖 **Groq Integration**: Uses Groq's Llama 3-8B-8192 model
- 🔍 **Semantic Search**: FAISS-based vector search
- 💬 **Interactive UI**: Beautiful Streamlit interface
- 📊 **Real-time Status**: Monitor system status
- 🎯 **Configurable**: Adjustable top-k retrieval settings

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the app**:
   ```bash
   streamlit run main.py
   ```

2. **Open browser** at `http://localhost:8501`

3. **Upload documents**:
   - Use file uploader for text files or PDFs
   - Or enter text directly

4. **Ask questions**:
   - Type your question
   - Get AI-generated answers

## Project Structure

```
RAG_without_framework/
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── src/
│   └── services/
│       ├── service1.py     # RAG service (chunking, embedding, FAISS)
│       └── llm_service.py  # Groq LLM integration
├── data/                   # Uploaded documents storage
├── database/               # FAISS index and embeddings storage
└── README.md              # This file
```

## Storage

- **FAISS Index**: Stored in `database/faiss_index.bin`
- **Documents**: Stored in `database/documents.json`
- **Embeddings**: Stored in `database/embeddings.pkl`
- **Uploaded Files**: Copies stored in `data/` folder

## Dependencies

- **Streamlit**: Web interface
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **Groq**: LLM API
- **PyPDF2**: PDF processing
- **NumPy**: Numerical operations

## API Key

The Groq API key is included directly in `src/services/llm_service.py`:
```python
self.api_key = ""
```

## License

This project is for educational and research purposes. 