from fastapi import HTTPException
from embeddings.openai_embeddings import embed_query_with_openai
from stores.pinecone_store import retrieve_from_pinecone_index
from stores.chroma_store import retrieve_from_chroma_collection
from stores.postgres_store import retrieve_from_pgvector
from models.ResponseModel import Chunk

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
            raise HTTPException(500, f"Error generating embeddings: {str(e)}")
    else:
        ## NOTE: Currently only openai is supported for embeddings
        raise HTTPException(501, "Embedding model not supported")
    

    ## Step 4: Add embeddings to vector store
    vectordb = request.vectordb_provider
    collection_name = request.collection_name
    min_similarity = request.min_similarity_threshold

    if vectordb == "pinecone":
        pinecone_apikey = request.pinecone_apikey
        try:
            result = retrieve_from_pinecone_index(
                query_vector= query_vector,
                index_name=collection_name,
                pinecone_apikey=pinecone_apikey
            )
            
            # Filter out chunks with similarity less than min_similarity
            ## NOT IMPLEMENTED YET

                        # Assuming response is the result from index.query() function of pinecone
            chunks = []

            for match in result["matches"]:
                chunk = Chunk(
                    chunk_id=match["id"],
                    chunk_text=match["text"],
                    score=match["score"]
                )
                chunks.append(chunk)
                
        except Exception as e:
            raise HTTPException(500, f"Error retrieving data from pinecone: {str(e)}")

    elif vectordb == "chroma":
        try:
            chroma_url = request.chroma_url
            chroma_port = request.chroma_port
            
            result = retrieve_from_chroma_collection(
                query_vector=query_vector,
                collection_name=collection_name,
                host_url=chroma_url,
                port=chroma_port
            )

            chunks = []

            for i in range(len(result["ids"][0])):
                if result["distances"][0][i] < min_similarity:
                    continue
                chunk = Chunk(
                    text=result["metadatas"][0][i]["text_segment"],
                    source=result["metadatas"][0][i]["source"]
                )
                chunks.append(chunk)   
            return chunks

        except Exception as e:
            raise HTTPException(500, f"Error adding data to chroma: {str(e)}")

    elif vectordb == "pgvector":
        try:
            postgres_host = request.postgres_host
            postgres_user = request.postgres_user
            postgres_password = request.postgres_password
            postgres_dbname = request.postgres_dbname
            postgres_table_name = request.postgres_table_name
            
            results = retrieve_from_pgvector(
                query_vector=query_vector,
                host=postgres_host,
                password=postgres_password,
                user=postgres_user,
                dbname=postgres_dbname,
                table_name=postgres_table_name
            )

            chunks = []
            for chunk in results:
                chunks.append(Chunk(
                    text=chunk["text_segment"],
                    source=chunk["source"]
                ))

            return chunks

        except Exception as e:
            raise HTTPException(500, f"Error adding data to pgvector: {str(e)}")
    else:
        raise HTTPException(400, f"Vector database type unidentified: {vectordb}")
