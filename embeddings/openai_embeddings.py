from fastapi import HTTPException
from openai import OpenAI
import asyncio
from models.VectorStoreRecord import VectorStoreRecord

# Function to get embeddings for multiple text chunks from OpenAI API (async version)
async def embed_with_openai(text_inputs: list[str], apikey: str, source: str) -> list[VectorStoreRecord]:
    print("Received call to generate embeddings")
    try:
        # Create openai client
        client = OpenAI(api_key=apikey)

        # Make the request to OpenAI to generate embeddings for all text chunks at once
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: client.embeddings.create(
            model="text-embedding-ada-002",  # This is the model for generating embeddings
            input=text_inputs  # Pass the array of text chunks directly
        ))

        # Process the response and create a list of embedding results
        results = []
        for idx, embedding_data in enumerate(response.data):
            result = VectorStoreRecord(
                embedding = embedding_data.embedding,
                text_segment = text_inputs[idx],
                source = source
            )
            results.append(result)

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
