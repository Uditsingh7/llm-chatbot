
import json
import argparse
import timeit
from rag.pipeline import build_rag_pipeline

## Get Rag Response

def get_rag_response(query, chain):
    """
    Get a response from the RAG model based on the query.
    
    Args:
        query (str): The input query to process.
        chain (RetrievalQA): The retrieval-based question answering chain.
    
    Returns:
        str: The generated response from the RAG model.
    """
    
    response = chain.invoke({"query": query})
    answer = response['result']
    
    start_index = answer.find("{")
    end_index = answer.rfind("}")
    
    if(start_index != -1 and end_index != -1 and end_index > start_index):
        json_fragment = answer[start_index:end_index + 1]
        
        try:
            ## convert extracted string to JSON
            json_data = json.loads(json_fragment)
            return json_data
        except json.JSONDecodeError:
            print("Error decoding JSON from the response.")
    else:
        print("No valid JSON fragment found in the response.")
    
    return answer  # Return None if no valid JSON fragment is found or if an error occurs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input', 
                        type=str, 
                        help='Enter the query to pass into the LLM',
                        default="What is the invoice number value?"                  
                        )
    
    args = parser.parse_args()
    
    start = timeit.default_timer()
    
    ## Build the RAG pipeline
    rag_chain = build_rag_pipeline()
    print("RAG pipeline built successfully.")
    ## Get the response from the RAG model
    response = get_rag_response(args.input, rag_chain)
    
    end = timeit.default_timer()
    
    print(f"Response: {response}")
    print('=' * 50)
    print(f"Time taken: {end - start:.2f} seconds")
    
    
    
    
    
    
        

