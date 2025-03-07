from pinecone import Pinecone

def add_to_pinecone_index(documents, index_name, pinecone_apikey, batch_size=100):
    print("Received call to add to store.")
    pc = Pinecone(api_key=pinecone_apikey)
    index = pc.Index(name=index_name)
    
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
