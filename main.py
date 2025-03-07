from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status
from models.RequestModel import VectorStoreSetupRequest, VectorStoreRetrieveRequest
from models.ResponseModel import RetrieveResponseModel, Chunk
from request_registry import RequestRegistry
from validate_request import missing_vectordb_params
from ingest import ingest_to_store
from retrieve import retrieve_from_store
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


## Initialize Registry to hold configurations for each request_id
request_details = RequestRegistry()


@app.post("/setup")
async def details(request: VectorStoreSetupRequest):
    # Check if the necessary properties are present in the request
    # Returns None if all properties are present, else returns an HTTPException
    http_exception = missing_vectordb_params(request)
    if http_exception is not None:
        return http_exception
    
    try:
        # Add request to the registry
        request_details.add_request(request)
    except:
        return HTTPException(400, "Request couldn't be processed")
    
    return status.HTTP_200_OK
    

@app.post("/upload")
async def upload(requestId: str = Form(...), file:UploadFile = File(...) ):

    # Retrieve the configurations for the requestId
    configurations = request_details.get_configurations(request_id=requestId)

    if configurations is None:
        return HTTPException(400, "RequestId not recognized or exceeded file count for requestId")
    else:
        # Add the file to the vector store
        try:
            response = await ingest_to_store(configurations, file)
            print(response)
        except Exception as e:
            return e
        
    return status.HTTP_201_CREATED


@app.post("/retrieve", response_model=None)
async def retrieve(request: VectorStoreRetrieveRequest):
    # Check if the necessary properties are present in the request
    # Returns None if all properties are present, else returns an HTTPException
    http_exception = missing_vectordb_params(request)
    if http_exception is not None:
        return http_exception
    
    else:
        # Retrieve the data from the vector store
        try:
            response = await retrieve_from_store(request)

            # Assuming response is the result from index.query() function of pinecone
            chunks = [Chunk(text=match['metadata']['text'], source=match['metadata']['source']) for match in response['matches']]
            return RetrieveResponseModel(query=request.user_query, retrieved_chunks=chunks)
            # return response
        except Exception as e:
            return e
