# 🤖 AI-ML Internship Projects - RAG & LangGraph Solutions

This repository contains three comprehensive AI/ML projects developed during the internship at Eminds, showcasing different approaches to building intelligent applications using modern AI frameworks and technologies.

## 📁 Project Overview

### 🏗️ **Project Architecture**

```
AI-ML-Internship-Eminds/
├── 📄 RAG_App_using_langchain/          # LangChain-based RAG system
├── 🔧 RAG_without_framework/            # Frameworkless RAG implementation
└── 🌤️ Weather_info_bot_using_LangGraph/ # LangGraph weather chatbot
```

---

## 🚀 **Project 1: RAG App using LangChain**

### 📋 **Description**
A sophisticated Retrieval-Augmented Generation (RAG) system built with LangChain framework, featuring PDF processing, vector embeddings, and intelligent question answering powered by Groq's fast LLM models.

### ✨ **Key Features**
- **PDF Document Processing**: Upload and extract text from PDF files
- **LangChain Integration**: Leverages LangChain's powerful RAG framework
- **Multiple LLM Models**: Support for various Groq models (llama3-8b-8192, mixtral-8x7b-32768, llama3-70b-8192)
- **FAISS Vector Store**: Fast and efficient similarity search
- **Dual Interface**: Both Streamlit UI and Flask API
- **Real-time Chat**: Interactive question-answering interface
- **Configurable Parameters**: Adjustable chunk size, overlap, and search results

### 🛠️ **Technology Stack**
- **Framework**: LangChain
- **UI**: Streamlit
- **API**: Flask
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace Sentence Transformers
- **LLM**: Groq API
- **PDF Processing**: pdfminer.six

### 🚀 **Quick Start**

#### **Docker Deployment (Recommended)**
```bash
cd RAG_App_using_langchain
echo "GROQ_API_KEY=your_api_key_here" > .env
docker-compose up -d
```

#### **Local Development**
```bash
cd RAG_App_using_langchain
pip install -r requirements.txt
python app.py  # Flask API
streamlit run main.py  # Streamlit UI
```

#### **API Usage**
```bash
# Upload text
curl -X POST http://localhost:5000/api/documents/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text content here"}'

# Query the system
curl "http://localhost:5000/api/query?question=What is AI?"
```

### 🌐 **Access Points**
- **Flask API**: http://localhost:5000
- **Streamlit UI**: http://localhost:8502 (Docker) / http://localhost:8501 (Local)
- **API Documentation**: http://localhost:5000/docs

---

## 🔧 **Project 2: RAG without Framework**

### 📋 **Description**
A clean, frameworkless implementation of a RAG system built from scratch, demonstrating core RAG concepts without external framework dependencies. Features direct integration with Groq API and custom vector operations.

### ✨ **Key Features**
- **Frameworkless Design**: Built from scratch without external RAG frameworks
- **Custom Implementation**: Direct control over every component
- **FAISS Integration**: Native FAISS vector store operations
- **Dual Interface**: Streamlit UI and Flask API
- **Text & PDF Support**: Upload and process various document types
- **Real-time Processing**: Immediate document processing and querying

### 🛠️ **Technology Stack**
- **Core**: Pure Python implementation
- **UI**: Streamlit
- **API**: Flask
- **Vector Store**: FAISS
- **Embeddings**: Sentence Transformers
- **LLM**: Groq API
- **PDF Processing**: PyPDF2

### 🚀 **Quick Start**

#### **Docker Deployment**
```bash
cd RAG_without_framework
echo "GROQ_API_KEY=your_api_key_here" > .env
docker-compose up -d
```

#### **Local Development**
```bash
cd RAG_without_framework
pip install -r requirements.txt
python app.py  # Flask API
streamlit run main.py  # Streamlit UI
```

#### **API Usage**
```bash
# Upload text
curl -X POST http://localhost:5000/api/documents/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text content here"}'

# Query the system
curl "http://localhost:5000/api/query?question=What is AI?"
```

### 🌐 **Access Points**
- **Flask API**: http://localhost:5000
- **Streamlit UI**: http://localhost:8503 (Docker) / http://localhost:8501 (Local)
- **API Documentation**: http://localhost:5000/docs

---

## 🌤️ **Project 3: Weather Info Bot using LangGraph**

### 📋 **Description**
An intelligent weather information chatbot built with LangGraph, featuring conversational AI capabilities, weather data integration, and a sophisticated workflow management system.

### ✨ **Key Features**
- **LangGraph Integration**: Advanced workflow management with LangGraph
- **Weather API Integration**: Real-time weather data retrieval
- **Conversational AI**: Natural language processing for weather queries
- **Memory Management**: Context-aware conversations
- **Workflow Visualization**: Visual representation of conversation flows
- **Multi-turn Conversations**: Support for complex weather-related discussions

### 🛠️ **Technology Stack**
- **Framework**: LangGraph
- **UI**: Streamlit
- **Weather API**: OpenWeatherMap (or similar)
- **LLM**: Groq API
- **Memory**: LangGraph memory systems
- **Workflow**: LangGraph state machines

### 🚀 **Quick Start**

#### **Docker Deployment**
```bash
cd Weather_info_bot_using_LangGraph
echo "GROQ_API_KEY=your_api_key_here" > .env
docker-compose up -d
```

#### **Local Development**
```bash
cd Weather_info_bot_using_LangGraph
pip install -r requirements.txt
streamlit run main.py
```

### 🌐 **Access Points**
- **Streamlit UI**: http://localhost:8501
- **Workflow Visualization**: Available in the UI

---

## 🔑 **Prerequisites**

### **Required API Keys**
1. **Groq API Key**: Get from [Groq Console](https://console.groq.com/)
2. **Weather API Key** (for Weather Bot): Get from [OpenWeatherMap](https://openweathermap.org/api)

### **System Requirements**
- Python 3.8+
- Docker (for containerized deployment)
- 4GB+ RAM (recommended)
- Internet connection for model downloads

---

## 🚀 **Quick Comparison**

| Feature | LangChain RAG | Frameworkless RAG | Weather Bot |
|---------|---------------|-------------------|-------------|
| **Framework** | LangChain | Custom | LangGraph |
| **Complexity** | Medium | Low | High |
| **Customization** | Limited | High | Medium |
| **Learning Value** | Framework usage | Core concepts | Workflow design |
| **API Support** | ✅ | ✅ | ❌ |
| **UI Support** | ✅ | ✅ | ✅ |
| **Docker Support** | ✅ | ✅ | ✅ |

---

## 🛠️ **Development Setup**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd AI-ML-Internship-Eminds
```

### **2. Set Up Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies for all projects
pip install -r RAG_App_using_langchain/requirements.txt
pip install -r RAG_without_framework/requirements.txt
pip install -r Weather_info_bot_using_LangGraph/requirements.txt
```

### **3. Configure API Keys**
```bash
# For each project, create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > RAG_App_using_langchain/.env
echo "GROQ_API_KEY=your_groq_api_key_here" > RAG_without_framework/.env
echo "GROQ_API_KEY=your_groq_api_key_here" > Weather_info_bot_using_LangGraph/.env
```

---

## 🧪 **Testing & Usage**

### **Testing All Projects**

#### **1. LangChain RAG**
```bash
cd RAG_App_using_langchain
python api_client_example.py
```

#### **2. Frameworkless RAG**
```bash
cd RAG_without_framework
python api_client_example.py
```

#### **3. Weather Bot**
```bash
cd Weather_info_bot_using_LangGraph
streamlit run main.py
```

### **API Testing Commands**
```bash
# Test health endpoints
curl http://localhost:5000/health  # LangChain RAG
curl http://localhost:5000/health  # Frameworkless RAG

# Test query endpoints
curl "http://localhost:5000/api/query?question=What is AI?"  # LangChain RAG
curl "http://localhost:5000/api/query?question=What is AI?"  # Frameworkless RAG
```

---

## 📊 **Performance & Monitoring**

### **Health Checks**
- **LangChain RAG**: `GET /health`
- **Frameworkless RAG**: `GET /health`
- **Weather Bot**: Built-in status indicators

### **Logging**
All projects include comprehensive logging for:
- API requests and responses
- Error tracking and debugging
- Performance metrics
- System status monitoring

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. API Key Errors**
```bash
# Check if API key is set correctly
cat .env  # Should show your Groq API key
```

#### **2. Port Conflicts**
```bash
# Check what's using the ports
lsof -i :5000
lsof -i :8501
lsof -i :8502
lsof -i :8503
```

#### **3. Docker Issues**
```bash
# Check Docker status
docker-compose ps
docker-compose logs -f
```

#### **4. Memory Issues**
- Reduce chunk size for large documents
- Use smaller models for faster processing
- Increase system RAM if needed

### **Debug Mode**
All projects support debug mode for detailed error information:
```bash
# Enable debug mode in app.py
debug=True
```

---

## 📚 **Learning Resources**

### **RAG Concepts**
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers](https://www.sbert.net/)

### **LangGraph**
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Workflow Design Patterns](https://langchain-ai.github.io/langgraph/tutorials/)

### **Groq API**
- [Groq Documentation](https://console.groq.com/docs)
- [Model Comparison](https://console.groq.com/docs/models)

---

## 🤝 **Contributing**

### **Development Workflow**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Code Standards**
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Write unit tests for new features

---

## 📄 **License**

This project is part of the AI-ML Internship at Eminds and is intended for educational and research purposes.

---

## 🙏 **Acknowledgments**

- **Eminds**: For providing the internship opportunity
- **LangChain**: For the powerful RAG framework
- **Groq**: For fast LLM inference
- **HuggingFace**: For embedding models
- **Streamlit**: For the web interface framework
- **FAISS**: For efficient vector similarity search

---

## 📞 **Support**

For questions, issues, or contributions:
- Create an issue in the repository
- Check the individual project README files
- Review the troubleshooting section above

---

**Happy Coding! 🚀** 