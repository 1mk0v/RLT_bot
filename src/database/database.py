from pymongo import MongoClient
from models import Request

class RLTDatabaseInterface:

    def __init__(self) -> None:
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['RLT_DB']
        self.collection = self.db['sample_collection']
    
    async def get(self, request:Request):
        return self.collection.find(
            {'dt': {
                "$lt": request.dt_upto,
                "$gte": request.dt_from
                }
            }
        )
