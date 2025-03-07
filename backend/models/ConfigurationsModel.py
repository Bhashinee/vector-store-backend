from pydantic import BaseModel, Field
from typing import Optional

class ConfigurationsModel(BaseModel):
    vectordb_provider: str = Field(..., description="The provider of the vector database (e.g., 'Chroma', 'Pinecone')")
    pinecone_apikey: Optional[str] = Field(None, description="API key for accessing the vector database provider")
    chroma_url: Optional[str] = Field(None, description="The URL for the Chroma vector database instance")
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
