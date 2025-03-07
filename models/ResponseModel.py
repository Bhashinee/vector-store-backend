from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    text: str
    source: str

class RetrieveResponseModel(BaseModel):
    query: str
    retrieved_chunks: List[Chunk]
