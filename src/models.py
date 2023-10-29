import datetime
from pydantic import BaseModel
from typing import List

class Request(BaseModel):
    dt_from:datetime.datetime
    dt_upto:datetime.datetime
    group_type:str


class Response(BaseModel):
    dataset:List[int]
    labels:List[datetime.datetime]