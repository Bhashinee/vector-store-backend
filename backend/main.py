from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.RequestModel import VectorStoreSetupRequest, VectorStoreRetrieveRequest
from models.ResponseModel import RetrieveResponseModel, Chunk
from request_registry import RequestRegistry
from validate_request import check_for_missing_params
from ingest import ingest_to_store
from retrieve import retrieve_from_store
import os

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
    _ = check_for_missing_params(request)
    
    try:
        # Add request to the registry
        request_details.add_request(request)
    except:
        raise HTTPException(400, "Request couldn't be processed")
    
    return status.HTTP_200_OK
    

@app.post("/upload")
async def upload(request_id: str = Form(...), file:UploadFile = File(...) ):

    print("***********NLTK_DATA***************", os.getenv('NLTK_DATA'))
    print("***********MPLCONFIGDIR***************", os.getenv('MPLCONFIGDIR'))

    # Retrieve the configurations for the requestId
    configurations = request_details.get_configurations(request_id=request_id)

    if configurations is None:
        raise HTTPException(400, "RequestId not recognized or exceeded file count for requestId")
    else:
        # Add the file to the vector store
        response = await ingest_to_store(configurations, file)
        return response


@app.post("/retrieve", response_model=None)
async def retrieve(request: VectorStoreRetrieveRequest):
    # Check if the necessary properties are present in the request
    # Raises HttpException if any parameters are missing
    _ = check_for_missing_params(request)
    
    # Retrieve the data from the vector store
    response = await retrieve_from_store(request)
    return RetrieveResponseModel(query=request.user_query, retrieved_chunks=response)
