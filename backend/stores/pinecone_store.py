from pinecone import Pinecone, ServerlessSpec
import time

def add_to_pinecone_index(documents, index_name, pinecone_apikey, batch_size=100):
    print("Received call to add to store.")
    pc = Pinecone(api_key=pinecone_apikey)

    try:
        # Check if the index exists, if not create it
        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=len(documents[0]["values"]),
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

        index = pc.Index(index_name)
    except Exception as e:
        print(f"Error creating index: {str(e)}")
        raise e

    
    # Calculate number of batches
    total_docs = len(documents)
    print(f"Total documents to upsert: {total_docs}")
    
    upsert_responses = []
    
    # Process documents in batches
    for i in range(0, total_docs, batch_size):
        batch = documents[i:i + batch_size]
        print(f"Upserting batch {i//batch_size + 1} with {len(batch)} documents")
        
        try:
            upsert_response = index.upsert(
                vectors=batch,
                namespace="ai"
            )
            upsert_responses.append(upsert_response)
            print(f"Successfully upserted batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error upserting batch {i//batch_size + 1}: {str(e)}")
            # You might want to handle this differently based on your needs
            upsert_responses.append({"error": str(e)})
    
    print(f"Completed upserting all documents to store. Total batches: {len(upsert_responses)}")
    
    return upsert_responses


def retrieve_from_pinecone_index(query_vector, index_name, pinecone_apikey, top_k=5):
    print("Received call to retrieve from store.")
    pc = Pinecone(api_key=pinecone_apikey)
    index = pc.Index(index_name)


    response = index.query(
            query_vector=query_vector,
            top_k=top_k,
            include_metadata=True
            )

    return response
