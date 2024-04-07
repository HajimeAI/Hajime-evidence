from typing import TypeVar


import time
from datetime import datetime
from ulid import ULID

from app.db.schemas import GenericResponseModel


T = TypeVar('T')


def get_unique_id():
    return str(ULID())
def get_current_time():
    return int(time.time() * 1000) + datetime.now().microsecond // 1000
def error_return(code, message, data:T=None):
    return GenericResponseModel(code=code, message= message,result=data)


def success_return(data: T=None):
    return GenericResponseModel(result=data)


def succ(data) -> T:
    data = {"code": 0, "message": "success", "result": data}
    return T(**data)