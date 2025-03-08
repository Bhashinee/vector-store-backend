import chromadb
from fastapi import HTTPException


def add_to_chroma_collection(embeddings, collection_name, host_url, port):
    chroma_client = chromadb.HttpClient(host=host_url, port=port)
    
    # Get the collection with collection_name if it exists,
    # else create a new collection of name collection_name
    collection = chroma_client.create_collection(collection_name, get_or_create=True)

    # Add the embeddings and metadata to the collection
    collection.add(
        ids=[embedding["id"] for embedding in embeddings],
        embeddings=[embedding["embedding"] for embedding in embeddings],
        metadatas=[embedding["metadata"] for embedding in embeddings]    
    )

    return True


def retrieve_from_chroma_collection(query_vector, collection_name, host_url, port, top_k=5):
    chroma_client = chromadb.HttpClient(host=host_url, port=port)

    try:
        collection = chroma_client.get_collection(collection_name)
    except ValueError:
        raise HTTPException(400, "Collection not found")
    
    # Query the collection with the query_vector
    response = collection.query(
        query_embeddings=query_vector,
        n_results=top_k
    )

    return response
