from pydantic import BaseModel, Field
from typing import Optional


# Model for the setup endpoint
class VectorStoreSetupRequest(BaseModel):
    request_id: str = Field(..., description="Unique identifier to link setup and upload requests")
    file_count: int = Field(1, description="The number of files uploaded with the request id")
    vectordb_provider: str = Field(..., description="The provider of the vector database (e.g., 'Chroma', 'Pinecone')")
    pinecone_apikey: Optional[str] = Field(None, description="API key for accessing the vector database provider")
    chroma_url: Optional[str] = Field(None, description="The URL for the Chroma vector database instance")
    chroma_port: Optional[int] = Field(None, description="The port Chroma is running on")
    postgres_host: Optional[str] = Field(None, description="Host of the Postgres Database")
    postgres_user: Optional[str] = Field(None, description="User of the Postgres Database")
    postgres_password: Optional[str] = Field(None, description="Password of the Postgres Database")
    postgres_dbname: Optional[str] = Field(None, description="Name of the Postgres Database")
    postgres_table_name: Optional[str] = Field(None, description="Name of the table in the Postgres Database")
    collection_name: str = Field(..., description="The name of the collection to store or query from in the vector DB")
    embedding_model: str = Field(..., description="The model used for embedding (e.g., OpenAI")
    embedding_model_apikey: str = Field(..., description="API key for accessing the embedding model")
    chunking_strategy: str = Field(..., description="Strategy for chunking the file or text (e.g., 'sentence', 'paragraph')")
    max_segment_size: int = Field(..., description="The maximum size of each chunk/segment (in characters or tokens)")
    max_overlap_size: int = Field(..., description="The maximum overlap size between chunks (in characters or tokens)")

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "file_count": 2,
                "vectordb_provider": "Postgres",
                "postgres_host": "localhost",
                "postgres_user": "user",
                "postgres_password": "password",
                "postgres_dbname": "my_database",
                "postgres_table_name": "my_table",
                "collection_name": "my_collection",
                "embedding_model": "OpenAI",
                "embedding_model_apikey": "your_embedding_model_apikey",
                "chunking_strategy": "sentence",
                "max_segment_size": 500,
                "max_overlap_size": 50
            }
        }

# Model for the /file-processing/upload endpoint (multipart/form-data fields)
class VectorStoreFileUploadRequest(BaseModel):
    request_id: str = Field(..., description="Unique identifier matching the setup request")
    file_type: str = Field(..., description="Name of the uploaded file")

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "file_type": "pdf"
            }
        }


# Model for the retrieve endpoint
class VectorStoreRetrieveRequest(BaseModel):
    vectordb_provider: str = Field(..., description="The provider of the vector database (e.g., 'Chroma', 'Pinecone')")
    pinecone_apikey: Optional[str] = Field(None, description="API key for accessing the vector database provider")
    chroma_url: Optional[str] = Field(None, description="The URL for the Chroma vector database instance")
    chroma_port: Optional[int] = Field(None, description="The port Chroma is running on")
    postgres_host: Optional[str] = Field(None, description="Host of the Postgres Database")
    postgres_user: Optional[str] = Field(None, description="User of the Postgres Database")
    postgres_password: Optional[str] = Field(None, description="Password of the Postgres Database")
    postgres_dbname: Optional[str] = Field(None, description="Name of the Postgres Database")
    postgres_table_name: Optional[str] = Field(None, description="Name of the table in the Postgres Database")
    collection_name: str = Field(..., description="The name of the collection to store or query from in the vector DB")
    embedding_model: str = Field(..., description="The model used for embedding (e.g., OpenAI")
    embedding_model_apikey: str = Field(..., description="API key for accessing the embedding model")
    user_query: str = Field(..., description="The query submitted by the user for which the similar text chunks from the vector store will be retrieved")
    max_retrieve_chunks: int = Field(..., description="The maximum number of chunks to retrieve from the vector store")
    min_similarity_threshold: float = Field(..., ge=0, le=1, description="The minimum similarity to the given embedding of the given query, each retrieved chunk must have. (Value between 0 and 1)")

    class Config:
        json_schema_extra = {
            "example": {
            "vectordb_provider": "Chroma",
            "pinecone_apikey": None,
            "chroma_url": "http://localhost:8000",
            "collection_name": "my_collection",
            "embedding_model": "OpenAI",
            "embedding_model_apikey": "your_embedding_model_apikey",
            "user_query": "What is the capital of France?",
            "max_retrieve_chunks": 5,
            "min_similarity_threshold": 0.75
            }
        }
