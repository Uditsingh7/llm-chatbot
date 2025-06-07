
from PyPDF2 import PdfReader
from rag.pipeline import build_rag_pipeline
import timeit
from main import get_rag_response
import streamlit as st
from dotenv import load_dotenv
from htmlTemplate import css
from ingest import run_injest




## get text from the pdf file
def get_pdf_text(pdf_docs: list[str]) -> str:
    """
    Extracts text content from a list of PDF documents.

    Args:
        pdf_docs: A list of file paths or data objects representing the PDF documents.

    Returns:
        A string containing the combined text content of all PDFs.
    """
    
    text = ''
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text  
    

## handle user input

def handle_user_input(user_question: str) -> None:
    """
    Processes user input and retrieves an answer using a RAG (Reader-Answer Generator) pipeline.

    Args:
        user_question: The user's question about the uploaded documents.

    Returns:
        None (modifies Streamlit app state with the answer and processing time).
    """
    
    start = timeit.default_timer()
    
    ## Build the RAG pipeline
    rag_chain = build_rag_pipeline()
    
    print("RAG pipeline built successfully.")
    
    ## Get the response from the RAG model
    response = get_rag_response(user_question, rag_chain)
    
    end = timeit.default_timer()
    
    st.write("Answer:", response)
    st.markdown(f"**Time to retrieve answer:** {end - start:.2f} seconds", unsafe_allow_html=True)
    
    
def main() -> None:
    """
    The main function of the Streamlit application.

    Loads environment variables, configures the Streamlit app layout,
    handles user interaction, and processes PDFs.
    """
    load_dotenv()
    
    st.set_page_config(page_title="Converge the stars of memory and reason", page_icon=":book:", layout="wide")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.header("Align vectors of memory and meaning in the Cosmic Archives 🛰️📄")
    user_question = st.text_input(
    "Query the Neural Codex of your PDFs:", 
    placeholder="E.g., What’s the invoice number?", 
    key="user_question"
    )
    
    if user_question:
        handle_user_input(user_question)
        
    with st.sidebar:
        st.subheader("Upload your PDF documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Ingest'", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if st.button("Ingest"):           
            with st.spinner("Ingesting documents..."): 
                ## Process the uploaded PDFs
                raw_text = get_pdf_text(pdf_docs)  
                run_injest(raw_text)
                st.success("Documents ingested successfully!")
                 
            

if __name__ == "__main__":
    main()