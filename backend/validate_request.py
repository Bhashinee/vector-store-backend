from fastapi import HTTPException
from models.RequestModel import VectorStoreSetupRequest


def check_for_missing_params(request: VectorStoreSetupRequest):
    if request.vectordb_provider == "pinecone":
        # Check that the pinecone apikey is present in the request
        if request.pinecone_apikey == "" or request.pinecone_apikey is None:
            raise HTTPException(status_code=400, detail="Pinecone apikey is required for pinecone vectordb")
    elif request.vectordb_provider == "chroma":
        # Check that the chroma url and port are present in the request
        if request.chroma_url == "" or request.chroma_url is None:
            raise HTTPException(status_code=400, detail="Chroma url is required for chroma vectordb")
        if request.chroma_port == "" or request.chroma_port is None:
            raise HTTPException(status_code=400, detail="Chroma port is required for chroma vectordb")
    elif request.vectordb_provider == "pgvector":
        # Check that the postgres host, user, password, dbname, and table name are present in the request
        if request.postgres_host == "" or request.postgres_host is None:
            raise HTTPException(status_code=400, detail="Postgres host is required for pgvector vectordb")
        if request.postgres_user == "" or request.postgres_user is None:
            raise HTTPException(status_code=400, detail="Postgres user is required for pgvector vectordb")
        if request.postgres_password == "" or request.postgres_password is None:
            raise HTTPException(status_code=400, detail="Postgres password is required for pgvector vectordb")
        if request.postgres_dbname == "" or request.postgres_dbname is None:
            raise HTTPException(status_code=400, detail="Postgres dbname is required for pgvector vectordb")
        if request.postgres_table_name == "" or request.postgres_table_name is None:
            raise HTTPException(status_code=400, detail="Postgres table name is required for pgvector vectordb")
    else:
        raise HTTPException(status_code=400, detail="Vector database type unidentified")
    return None
