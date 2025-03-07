from fastapi import HTTPException
from embeddings.openai_embeddings import embed_query_with_openai
from stores.pinecone_store import retrieve_from_pinecone_index
from stores.chroma_store import add_to_chroma_collection
from stores.postgres_store import add_to_pgvector
from parser import parse_content
from chunker import chunk_data

from models.RequestModel import VectorStoreRetrieveRequest


async def retrieve_from_store(request: VectorStoreRetrieveRequest):
    ## Step 1: Generate embedding for the query
    # Get the embedding model and apikey from request
    embedding_model = request.embedding_model
    embedding_model_apikey = request.embedding_model_apikey

    if embedding_model == "openai":
        try:
            query_vector = await embed_query_with_openai(
                query=request.user_query,
                apikey=embedding_model_apikey
            )
        except Exception as e:
            print(e)
            return HTTPException(500, f"Error generating embeddings: {str(e)}")
    else:
        ## NOTE: Currently only openai is supported for embeddings
        return HTTPException(501, "Embedding model not supported")
    

    ## Step 4: Add embeddings to vector store
    vectordb = request.vectordb_provider
    collection_name = request.collection_name

    if vectordb == "pinecone":
        pinecone_apikey = request.pinecone_apikey
        try:
            result = retrieve_from_pinecone_index(
                query_vector= query_vector,
                index_name=collection_name,
                pinecone_apikey=pinecone_apikey
            )
            print(result)
            return result
        except Exception as e:
            return HTTPException(500, f"Error retrieving data from pinecone: {str(e)}")

    elif vectordb == "chroma":
        try:
            chroma_url = request.chroma_url
            chroma_port = request.chroma_port
            
            raise NotImplementedError("Chroma retrieval not implemented")
        except Exception as e:
            return HTTPException(500, f"Error adding data to chroma: {str(e)}")

    elif vectordb == "pgvector":
        try:
            postgres_host = request.postgres_host
            postgres_user = request.postgres_user
            postgres_password = request.postgres_password
            postgres_dbname = request.postgres_dbname
            postgres_table_name = request.postgres_table_name
            
            raise NotImplementedError("Postgres retrieval not implemented")
        except Exception as e:
            return HTTPException(500, f"Error adding data to pgvector: {str(e)}")
    else:
        return HTTPException(400, f"Vector database type unidentified: {vectordb}")

    # Step 5: Return response to the user
    return {"message": "Added data to vector store successfully"}
