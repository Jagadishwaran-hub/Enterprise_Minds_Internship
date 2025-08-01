# 📄 RAG-based PDF Chatbot using LangChain and Groq

A powerful Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them through natural language queries. Built with Streamlit, LangChain, and powered by Groq's fast LLM models.

## 🚀 Features

- **PDF Document Processing**: Upload and extract text from PDF files
- **Intelligent Text Chunking**: Configurable chunk size and overlap for optimal processing
- **Vector Embeddings**: Uses HuggingFace sentence transformers for semantic search
- **FAISS Vector Store**: Fast and efficient similarity search
- **Multiple LLM Models**: Support for various Groq models:
  - `llama3-8b-8192` (default)
  - `mixtral-8x7b-32768`
  - `llama3-70b-8192`
- **Interactive Web Interface**: User-friendly Streamlit dashboard
- **Real-time Chat**: Ask questions about your PDF content
- **Configurable Parameters**: Adjust chunk size, overlap, and search results

## 🏗️ Architecture

The application follows a modular service-oriented architecture:

```
src/
├── services/
│   ├── pdf_service.py      # PDF processing and text extraction
│   ├── vector_service.py   # Vector embeddings and FAISS operations
│   └── llm_service.py      # LLM integration with Groq
└── routers/               # API routing (if needed)
```

### Core Components

1. **PDFService**: Handles PDF upload, text extraction, and chunking
2. **VectorService**: Manages embeddings and FAISS vector store operations
3. **LLMService**: Interfaces with Groq API for question answering

## 📋 Prerequisites

- Python 3.8+
- Groq API key (get one from [Groq Console](https://console.groq.com/))
- Internet connection for model downloads

## 🛠️ Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd RAG_App_using_langchain
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
   - Open your browser and go to `http://localhost:8501`

### Option 2: Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd RAG_App_using_langchain
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Groq API key**:
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Update the `groq_api_key` in `src/services/llm_service.py` (line 12)

## 🚀 Usage

### Docker Deployment
1. **Start the application**:
   ```bash
   docker-compose up -d
   ```

2. **Access the applications**:
   - **Flask API**: `http://localhost:5000`
   - **Streamlit UI**: `http://localhost:8502`

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
- `POST /api/documents/upload` - Upload PDF files
- `POST /api/documents/text` - Upload text content
- `POST /api/query` - Query the RAG system
- `PUT /api/model` - Update LLM model
- `GET /api/config` - Get configuration
- `DELETE /api/documents` - Clear all documents

3. **Upload a PDF**:
   - Click "Choose a PDF file" in the left column
   - Select your PDF document
   - Click "Process PDF" to extract and chunk the text

4. **Configure settings** (optional):
   - Select your preferred LLM model
   - Adjust chunk size (500-2000 characters)
   - Set chunk overlap (50-500 characters)
   - Configure number of search results (1-10)

5. **Start chatting**:
   - Type your question in the chat interface
   - Click "Ask" to get an answer based on your PDF content

## ⚙️ Configuration

### Model Selection
- **llama3-8b-8192**: Fast, good for general queries
- **mixtral-8x7b-32768**: Balanced performance and quality
- **llama3-70b-8192**: Highest quality, slower response

### Chunk Parameters
- **Chunk Size**: Determines how text is split (default: 1000 characters)
- **Chunk Overlap**: Ensures context continuity between chunks (default: 200 characters)
- **Search Results (k)**: Number of similar documents retrieved (default: 4)

## 📁 Project Structure

```
RAG_App_using_langchain/
├── main.py                 # Main Streamlit application
├── app.py                  # Flask API application
├── api_client_example.py   # Example API client
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore patterns
├── run-docker.sh          # Docker runner script
├── data/                  # PDF uploads and storage
│   ├── Test.pdf
│   └── test2.pdf
├── database/              # Vector store and embeddings
│   └── faiss_index/
└── src/
    ├── services/
    │   ├── pdf_service.py
    │   ├── vector_service.py
    │   └── llm_service.py
    └── routers/
        ├── __init__.py    # Router package init
        └── router.py      # Flask API router
```

## 🔧 Dependencies

- **streamlit**: Web interface framework
- **flask**: API framework
- **flask-cors**: Cross-origin resource sharing
- **pdfminer.six**: PDF text extraction
- **langchain**: RAG framework and utilities
- **langchain-community**: Community integrations
- **langchain-huggingface**: HuggingFace embeddings
- **langchain-groq**: Groq LLM integration
- **sentence-transformers**: Text embeddings
- **faiss-cpu**: Vector similarity search

## 🎯 How It Works

1. **Document Processing**: PDF is uploaded and text is extracted using pdfminer
2. **Text Chunking**: Raw text is split into manageable chunks with configurable overlap
3. **Embedding Generation**: Text chunks are converted to vector embeddings using sentence transformers
4. **Vector Storage**: Embeddings are stored in a FAISS index for fast similarity search
5. **Query Processing**: User questions are embedded and similar chunks are retrieved
6. **Answer Generation**: Retrieved chunks are sent to Groq LLM with the question for context-aware answers

## 🔒 Security Notes

- The current implementation includes a hardcoded API key in the code
- For production use, consider using environment variables or secure key management
- Never commit API keys to version control
- **Docker users**: Use the `.env` file to securely store your Groq API key

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: 
   - Local: Ensure your Groq API key is correctly set in `llm_service.py`
   - Docker: Check your `.env` file has the correct `GROQ_API_KEY`
2. **Port Conflicts**: 
   - Local: Ensure ports 5000 and 8501 are available
   - Docker: API runs on port 5000, UI on port 8502
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
docker-compose exec rag-langchain-api bash
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: 
   - Local: Ensure your Groq API key is correctly set in `llm_service.py`
   - Docker: Check your `.env` file has the correct `GROQ_API_KEY`
2. **Model Download Issues**: Check your internet connection for embedding model downloads
3. **Memory Issues**: Reduce chunk size for large documents
4. **Slow Responses**: Try a smaller model or reduce search results
5. **Docker Issues**: 
   - Ensure Docker is running
   - Check if port 8501 is available
   - Use `docker-compose logs` to view error messages

### Performance Tips

- Use smaller chunk sizes for faster processing
- Reduce the number of search results (k) for quicker responses
- Choose appropriate models based on your needs (speed vs. quality)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the AI-ML Internship at Eminds.

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Groq](https://groq.com/) for fast LLM inference
- Uses [Streamlit](https://streamlit.io/) for the web interface
- Vector embeddings by [HuggingFace](https://huggingface.co/)

---

**Note**: This application is designed for educational and research purposes. Ensure you have proper permissions for any documents you process.
