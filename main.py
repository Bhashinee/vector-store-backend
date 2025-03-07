from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status
from models.RequestModel import VectorStoreSetupRequest, VectorStoreRetrieveRequest
from models.ResponseModel import RetrieveResponseModel
from request_registry import RequestRegistry
from process import add_to_store

app = FastAPI()


## Initialize Registry to hold configurations for each request_id
request_details = RequestRegistry()


@app.post("/setup")
async def details(request: VectorStoreSetupRequest):
    try:
        request_details.add_request(request)
    except:
        return HTTPException(400, "Request couldn't be processed")
    return status.HTTP_202_ACCEPTED
    

@app.post("/upload")
async def upload(requestId: str = Form(...), file:UploadFile = File(...) ):

    # Retrieve the configurations for the requestId
    configurations = request_details.get_configurations(request_id=requestId)

    if configurations is None:
        return HTTPException(400, "RequestId not recognized or exceeded file count for requestId")
    else:
        # Add the file to the vector store
        try:
            response = await add_to_store(configurations, file.file)
        except NotImplementedError:
            return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_201_CREATED


@app.post("/retrieve")
async def retrieve(request: VectorStoreRetrieveRequest) -> RetrieveResponseModel:
    return "Received API Call to /retrieve"
