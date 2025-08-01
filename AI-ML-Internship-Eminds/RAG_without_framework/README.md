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

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd RAG_without_framework
   ```

2. **Set up environment variables**:
   ```bash
   # Create .env file with your Groq API key
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```

3. **Run with Docker**:
   ```bash
   # Using the provided script
   chmod +x run-docker.sh
   ./run-docker.sh
   
   # Or manually with docker-compose
   docker-compose up -d
   ```

4. **Access the application**:
   - Open your browser and go to `http://localhost:8502`

### Option 2: Local Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Docker Deployment
1. **Start the app**:
   ```bash
   docker-compose up -d
   ```

2. **Access the applications**:
   - **Flask API**: `http://localhost:5000`
   - **Streamlit UI**: `http://localhost:8503`

### Local Development

#### Flask API
1. **Start the API**:
   ```bash
   python app.py
   ```

2. **Access the API** at `http://localhost:5000`

#### Streamlit UI
1. **Start the UI**:
   ```bash
   streamlit run main.py
   ```

2. **Open browser** at `http://localhost:8501`

### API Usage

#### Example API Client
```bash
python api_client_example.py
```

#### API Endpoints

- `GET /health` - Health check
- `GET /api/status` - System status
- `POST /api/documents/upload` - Upload PDF/TXT files
- `POST /api/documents/text` - Upload text content
- `POST /api/query` - Query the RAG system
- `GET /api/documents` - Get document information
- `DELETE /api/documents` - Clear all documents
- `GET /api/config` - Get configuration
- `PUT /api/config` - Update configuration

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
├── app.py                   # Flask API application
├── api_client_example.py    # Example API client
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Docker ignore patterns
├── run-docker.sh           # Docker runner script
├── src/
│   ├── services/
│   │   ├── service1.py     # RAG service (chunking, embedding, FAISS)
│   │   └── llm_service.py  # Groq LLM integration
│   └── routers/
│       ├── __init__.py     # Router package init
│       └── router.py       # Flask API router
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
- **Flask**: API framework
- **Flask-CORS**: Cross-origin resource sharing
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **Groq**: LLM API
- **PyPDF2**: PDF processing
- **NumPy**: Numerical operations
- **Requests**: HTTP client (for API client)

## API Key

The Groq API key is included directly in `src/services/llm_service.py`:
```python
self.api_key = ""
```

**For Docker users**: Use the `.env` file to securely store your Groq API key instead of hardcoding it in the source code.

## Troubleshooting

### Common Issues

1. **API Key Error**: 
   - Local: Ensure your Groq API key is correctly set in `llm_service.py`
   - Docker: Check your `.env` file has the correct `GROQ_API_KEY`
2. **Port Conflicts**: 
   - Local: Ensure port 8501 is available
   - Docker: The app runs on port 8502 to avoid conflicts
3. **Model Download Issues**: Check your internet connection for embedding model downloads
4. **Memory Issues**: Reduce chunk size for large documents

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Access container shell
docker-compose exec rag-frameworkless bash
```

## License

This project is for educational and research purposes. 