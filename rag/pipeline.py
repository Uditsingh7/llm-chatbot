from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
import box
import yaml
import warnings
# Suppress warnings from LangChain
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

## loading the embedding model
def load_embedding_model(model_name, normalize_embedding=True, device="cpu"):
    """
    Loads a Hugging Face embedding model.

    Args:
        model_name (str): Name of the Hugging Face model to load (e.g., "sentence-transformers/all-mpnet-base-v2").
        
        normalize_embedding (bool, optional): Whether to normalize the embeddings during encoding. Defaults to True.
        When you normalize an embedding vector, you scale it so that its length (or norm) becomes 1.
        All vectors lie on the unit hypersphere (in embedding space).
        The cosine similarity becomes equivalent to the dot product.
        Some search engines (like FAISS or ChromaDB) assume or require normalized vectors for cosine search.
        
        device (str, optional): Device to use for model inference (e.g., "cpu" or "cuda"). Defaults to "cpu".

    Returns:
        HuggingFaceEmbeddings: The loaded embedding model.
    """
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": normalize_embedding}
    )
    return embeddings


## loading the retireval model
def load_retrieval_model(embeddings, store_path, collection_name, vector_space, num_results=2):
    """
    Loads a retriever from a Chroma vector store.

    Args:
        embeddings (HuggingFaceEmbeddings): The embedding model to use for encoding documents.
        store_path (str): Path to the directory where the vector store persists data.
        collection_name (str): Name of the collection within the vector store.
        vector_space (str): Type of vector space used in the collection (e.g., "hnsw", "lsh", "cosine").
        num_results (int, optional): Number of documents to retrieve for each query. Defaults to 1.

    Returns:
        RetrievalQA: The loaded retriever.
    """
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=store_path,
        collection_metadata={"hnsw:space": vector_space},
        embedding_function=embeddings    
    )
    
    retriever = vector_store.as_retriever(
        search_kwargs = {
            "k": num_results,
        }
    )
    
    return retriever
   

## loading the prompt template
def load_prompt_template():
    """
    Loads a PromptTemplate object for guiding the large language model during retrieval-based QA.

    Returns:
        PromptTemplate: The loaded prompt template.
    """
    template = """Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )
    return prompt

## laoding the qa chain
def load_qa_chain(retriever, llm, prompt_template):
    """
    Loads a RetrievalQA chain for performing retrieval-based question answering.

    Args:
        retriever (RetrievalQA): The retriever to use for retrieving relevant documents.
        llm (Ollama): The large language model to use for answering the question.
        prompt (PromptTemplate): The prompt template to guide the LLM.

    Returns:
        RetrievalQA: The loaded QA chain.
    """
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )
    return qa_chain


## Building the RAG pipeline
def build_rag_pipeline():
    
    ## import config variables
    with open("config.yml", 'r', encoding='utf-8') as file:
        cfg = box.Box(yaml.safe_load(file))
        
    ## load embedding model
    print("Loading embedding model...")
    
    embeddings = load_embedding_model(
        model_name=cfg.EMBEDDINGS,
        normalize_embedding=cfg.NORMALIZE_EMBEDDINGS,
        device=cfg.DEVICE
    )
    
    ## load retriever
    print("Loading retriever...")
    retriever = load_retrieval_model(
        embeddings=embeddings,
        store_path = cfg.VECTOR_DB,
        collection_name = cfg.COLLECTION_NAME,
        vector_space = cfg.VECTOR_SPACE,
        num_results = cfg.NUM_RESULTS
    )
    
    ## load prompt template
    print("Loading prompt template...")
    prompt_template = load_prompt_template()
    
    ## load llm model
    print("Loading LLM model...")
    
    ## verbose=False Don’t print extra logs or debug messages during execution.   
    llm = OllamaLLM(
        model=cfg.LLM,
        temperature=cfg.TEMPERATURE,
        verbose=False  # Set verbose to False to suppress extra logs     
    )
    
    ## load qa chain
    print("Loading QA chain...")
    qa_chain = load_qa_chain(
        retriever=retriever,
        llm=llm,
        prompt_template=prompt_template
    )
    print("RAG pipeline built successfully!")
    return qa_chain

