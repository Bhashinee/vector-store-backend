import uuid

class VectorStoreRecord():
    def __init__(self, embedding, source, text_segment):
        self.embedding = embedding
        self.source = source
        self.text_segment = text_segment


    def to_pinecone_format(self):
        # Add a random id
        id = str(uuid.uuid4())
        pinecone_document =  {
            "id": id,
            "values": self.embedding,
            "metadata": {
                "source": self.source,
                "text_segment": self.text_segment
            }
        }

        return pinecone_document
    

    def to_chroma_format(self):
        chroma_format = {
            "id": str(uuid.uuid4()),
            "embedding": self.embedding,
            "metadata": {
                "source": self.source,
                "text_segment": self.text_segment
            }
        }

        return chroma_format
    

    def to_pgvector_format(self):
        pgvector_format = {
            "embedding": self.embedding,
            "text_segment": self.text_segment,
            "source": self.source
        }

        return pgvector_format
