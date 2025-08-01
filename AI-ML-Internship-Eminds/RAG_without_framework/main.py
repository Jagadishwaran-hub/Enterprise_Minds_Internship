import streamlit as st
import time
from src.services.service1 import RAGService
import os

# Page configuration
st.set_page_config(
    page_title="RAG with Groq & Llama 3-8B-8192",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize RAG service
@st.cache_resource
def initialize_rag_service():
    """Initialize the RAG service with caching"""
    rag_service = RAGService()
    rag_service.initialize()
    return rag_service

# Initialize the service
rag_service = initialize_rag_service()

# Main title
st.title("🤖 RAG System with Groq & Llama 3-8B-8192")
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")

    # Model information
    st.subheader("Model Info")
    status = rag_service.get_status()
    st.write(f"**Index Status:** {status['index_status']}")
    st.write(f"**Embedding Model:** {status['embedding_model']}")

    st.write(f"**LLM:** {status['llm_info']['model_type']}")
    st.write(f"**Device:** {status['llm_info']['device']}")

    # Top-k setting
    top_k = 3

    # Clear documents button

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📄 Upload Documents")

    uploaded_file = st.file_uploader(
        "Choose a text file or PDF",
        type=["txt", "pdf"],
        help="Upload a text or PDF file to add to the knowledge base"
    )

    if uploaded_file is not None:
        if st.button("📤 Process Document"):
            with st.spinner("Processing document..."):
                try:
                    if uploaded_file.type == "application/pdf":
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        text_content = ""
                        for page in pdf_reader.pages:
                            text_content += page.extract_text()
                    else:
                        text_content = uploaded_file.read().decode("utf-8")

                    documents_added = rag_service.add_documents(
                        [text_content], [uploaded_file.name]
                    )

                    st.success(f"✅ Successfully processed {uploaded_file.name}")
                    st.info(f"Added {documents_added} document chunks to the knowledge base")
                    time.sleep(1)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

    st.subheader("Or enter text directly:")
    text_input = st.text_area("Enter your text here", height=150)

    if st.button("📝 Add Text"):
        if text_input.strip():
            with st.spinner("Processing text..."):
                try:
                    documents_added = rag_service.add_documents(
                        [text_input], ["manual_input"]
                    )
                    st.success("✅ Successfully added text")
                    st.info(f"Added {documents_added} document chunks to the knowledge base")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing text: {str(e)}")
        else:
            st.warning("Please enter some text")

with col2:
    st.header("❓ Ask Questions")

    question = st.text_input(
        "Enter your question:",
        placeholder="What would you like to know about the uploaded documents?"
    )

    if st.button("🔍 Get Answer", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    answer, sources, confidence = rag_service.query(question, top_k)

                    st.subheader("💡 Answer")
                    st.write(answer)


                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")

# Document information section

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit • Powered by Groq & Llama 3-8B-8192 • RAG System</p>
    </div>
    """,
    unsafe_allow_html=True
)
