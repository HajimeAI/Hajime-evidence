from typing import TypeVar, Generic

from pydantic import BaseModel
T = TypeVar('T')


class GenericResponseModel(BaseModel, Generic[T]):
    code: int = 0
    message: str = ""
    result: T = None


class EvidenceDataModel(BaseModel):
    task_id: str
    data: str
    data_hash: str


class EvidenceDataInputModel(BaseModel):
    task_id: str
    data: str
    node_id:str=""

class TaskQueryModel(BaseModel):
    task_id: str
