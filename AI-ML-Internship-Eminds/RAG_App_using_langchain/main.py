import streamlit as st
import os
import sys

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.pdf_service import PDFService
from src.services.vector_service import VectorService
from src.services.llm_service import LLMService

# Page configuration
st.set_page_config(page_title="RAG PDF Chatbot", layout="wide")
st.title("📄 RAG-based PDF Chatbot using Groq")

# Initialize session state
if 'vector_service' not in st.session_state:
    st.session_state.vector_service = None
if 'llm_service' not in st.session_state:
    st.session_state.llm_service = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_options = ["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]
    selected_model = st.selectbox("Select LLM Model", model_options, index=0)
    
    # Chunk size configuration
    chunk_size = st.slider("Chunk Size", min_value=500, max_value=2000, value=1000, step=100)
    chunk_overlap = st.slider("Chunk Overlap", min_value=50, max_value=500, value=200, step=50)
    
    # Similarity search parameters
    k_results = st.slider("Number of similar documents (k)", min_value=1, max_value=10, value=4, step=1)
    
    # Update services if model changed
    if st.button("Update Model"):
        try:
            st.session_state.llm_service = LLMService(model_name=selected_model)
            st.success(f"Model updated to {selected_model}")
        except Exception as e:
            st.error(f"Error updating model: {str(e)}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file
                    temp_path = PDFService.save_uploaded_file(uploaded_file)
                    
                    # Extract text
                    raw_text = PDFService.extract_text_from_pdf(temp_path)
                    text_chunks = PDFService.get_text_chunks(raw_text, chunk_size, chunk_overlap)
                    
                    # Create vector store
                    st.session_state.vector_service = VectorService()
                    vector_store = st.session_state.vector_service.create_vector_store(text_chunks)
                    
                    # Initialize LLM service
                    st.session_state.llm_service = LLMService(model_name=selected_model)
                    
                    # Save vector store
                    save_path = st.session_state.vector_service.save_vector_store()
                    
                    # Cleanup temp file
                    # PDFService.cleanup_temp_file(temp_path)
                    
                    st.session_state.pdf_processed = True
                    st.success(f"PDF processed successfully! Created {len(text_chunks)} text chunks.")
                    
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")

with col2:
    st.header("💬 Chat Interface")
    
    if st.session_state.pdf_processed and st.session_state.vector_service:
        query = st.text_input("Ask something about the PDF")
        
        if query and st.button("Ask"):
            with st.spinner("Generating answer..."):
                try:
                    # Perform similarity search
                    docs = st.session_state.vector_service.similarity_search(query, k_results)
                    
                    # Get LLM response
                    response = st.session_state.llm_service.get_response(docs, query)
                    
                    # Display response
                    st.subheader("📢 Answer")
                    st.write(response)
                    
                    # Display model info
                    model_info = st.session_state.llm_service.get_model_info()
                    st.caption(f"Model: {model_info['model_name']} | Provider: {model_info['provider']}")
                    
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
    else:
        st.info("Please upload and process a PDF first to start chatting.")


# Display system status
if st.session_state.vector_service:
    st.sidebar.markdown("---")
    st.sidebar.header("📊 System Status")
    
    
    if st.session_state.llm_service:
        model_info = st.session_state.llm_service.get_model_info()
        st.sidebar.info(f"LLM Model: {model_info['model_name']}")
