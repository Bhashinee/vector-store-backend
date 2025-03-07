### Manage the requestIds for the requests made to the server

from models.RequestModel import VectorStoreSetupRequest

class RequestRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestRegistry, cls).__new__(cls)
            cls._instance.request_data = {}
        return cls._instance

    def add_request(self, request: VectorStoreSetupRequest):
        request_id = request.request_id
        file_count = request.file_count

        
        config = {key: value for key, value in request.__dict__.items() if key not in ['request_id', 'file_count']}


        self.request_data[request_id] = {
            'file_count': file_count,
            'configurations': config
        }

    def get_configurations(self, request_id: str):
        if request_id in self.request_data:
            self.request_data[request_id]['file_count'] -= 1
            configurations = self.request_data[request_id]['configurations']
            if self.request_data[request_id]['file_count'] == 0:
                del self.request_data[request_id]
            return configurations
        return None

    def get_request_ids(self):
        return list(self.request_data.keys())
