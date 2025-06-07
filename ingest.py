"""
This script ingests text documents into a vector store for efficient retrieval and semantic search.

It leverages the LangChain library for text splitting, embedding generation, and vector store creation.
"""

import box
import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import shutil


def run_injest(documents):
    """
    Ingests the provided documents into a LangChain vector store.

    Args:
        documents: A list of text documents to be ingested.
    """
    
    ## Load configuration from YAML file
    with open("config.yml", 'r', encoding='utf-8') as file:
        cfg = box.Box(yaml.safe_load(file))
        
    ## Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE,
        chunk_overlap=cfg.CHUNK_OVERLAP,
        # length_function=len
    )
    
    splits = text_splitter.split_text(documents)
    texts = text_splitter.create_documents(splits)
    print(f"Number of chunks created: {len(texts)}")
    
    ## Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.EMBEDDINGS,
        encode_kwargs={
            'normalize_embeddings':cfg.NORMALIZE_EMBEDDINGS
        },
        model_kwargs={
            'device': cfg.DEVICE
        }
    )
    
    ## Create or clear the vector store directory
    
    ## shutil: A standard Python module that provides high-level operations on files and directories.
    ## shutil.rmtree: Recursively deletes a folder and all its contents (files and subfolders).
    
    shutil.rmtree(cfg.VECTOR_DB, ignore_errors=True)
    print(f"Cleared vector store directory: {cfg.VECTOR_DB}")
    
    ## Create the vector store
    vector_store = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=cfg.VECTOR_DB,
        collection_name=cfg.COLLECTION_NAME,
        collection_metadata={
            "hnsw:space": cfg.VECTOR_SPACE ### Configure HNSW indexing
        }
    )
    print(f"Vector store created with {len(texts)} documents.")
    
    
if __name__ == "__main__":
    run_injest()
        
        
         
    
    
    
    
        
    
    
        
    
        
    
    