
import PdfReader
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
            text += page.extract_text() + '\n'
    return text.strip()  # Return the combined text, removing any leading/trailing whitespace
    

## handle user input

def handle_user_input(user_question: str) -> None:
    """
    Processes user input and retrieves an answer using a RAG (Reader-Answer Generator) pipeline.

    Args:
        user_question: The user's question about the uploaded documents.

    Returns:
        None (modifies Streamlit app state with the answer and processing time).
    """