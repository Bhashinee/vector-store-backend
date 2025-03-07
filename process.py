from fastapi import HTTPException
from embeddings.openai_embeddings import embed_with_openai
from stores.pinecone_store import add_to_pinecone_index
from stores.chroma_store import add_to_chroma_collection
from stores.postgres_store import add_to_pgvector
from parser import parse_content
from chunker import chunk_data

from models.ConfigurationsModel import ConfigurationsModel


async def add_file_to_store(configurations: ConfigurationsModel, file):

    ## Step 1: Parse the content
    input_text = parse_content(file.file)

    ## Step 2: Chunk the data
    # Get the parameters from the configurations
    chunk_type = configurations["chunking_strategy"]
    max_chunk_size = configurations["max_segment_size"]
    overlap = configurations["max_overlap_size"]

    try:
        chunked_text = chunk_data(
            data=input_text,
            chunk_type=chunk_type,
            chunk_size=max_chunk_size,
            overlap=overlap
            )
    except Exception as e:
        return HTTPException(500, f"Error chunking data, {str(e)}")

    ## Step 3: Generate embeddings
    # Get the embedding model and apikey from configurations
    embedding_model = configurations["embedding_model"]
    embedding_model_apikey = configurations["embedding_model_apikey"]

    if embedding_model == "openai":
        try:
            embeddings = await embed_with_openai(
                text_inputs=chunked_text,
                apikey=embedding_model_apikey,
                source=file.filename
            )
        except Exception as e:
            return HTTPException(500, f"Error generating embeddings: {str(e)}")
    else:
        ## NOTE: Currently only openai is supported for embeddings
        return HTTPException(501, "Embedding model not supported")
    

    ## Step 4: Add embeddings to vector store
    vectordb = configurations["vectordb_provider"]
    collection_name = configurations["collection_name"]

    if vectordb == "pinecone":
        documents = [embedding.to_pinecone_format() for embedding in embeddings]
        pinecone_apikey = configurations["pinecone_apikey"]
        try:
            add_to_pinecone_index(
                documents=documents,
                index_name=collection_name,
                pinecone_apikey=pinecone_apikey
            )
        except Exception as e:
            return HTTPException(500, f"Error adding data to pinecone: {str(e)}")

    elif vectordb == "chroma":
        try:
            embeddings = [embedding.to_chroma_format() for embedding in embeddings]
            chroma_url = configurations["chroma_url"]
            chroma_port = configurations["chroma_port"]
            add_to_chroma_collection(
                embeddings=embeddings,
                collection_name=collection_name,
                host_url=chroma_url,
                port=chroma_port
            )
        except Exception as e:
            return HTTPException(500, f"Error adding data to chroma: {str(e)}")

    elif vectordb == "pgvector":
        try:
            embeddings = [embedding.to_pgvector_format() for embedding in embeddings]
            postgres_host = configurations["postgres_host"]
            postgres_port = configurations["postgres_port"]
            postgres_user = configurations["postgres_user"]
            postgres_password = configurations["postgres_password"]
            postgres_dbname = configurations["postgres_dbname"]
            postgres_table_name = configurations["postgres_table_name"]
            add_to_pgvector(
                embeddings=embeddings,
                host=postgres_host,
                port=postgres_port,
                password=postgres_password,
                user=postgres_user,
                dbname=postgres_dbname,
                table_name=postgres_table_name
            )
        except Exception as e:
            return HTTPException(500, f"Error adding data to pgvector: {str(e)}")
    else:
        return HTTPException(400, f"Vector database type unidentified: {vectordb}")

    # Step 5: Return response to the user
    return {"message": "Added data to vector store successfully"}
