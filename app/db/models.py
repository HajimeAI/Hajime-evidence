import asyncio
import base64
import json
from hashlib import sha256
from typing import Any

import math
from beanie import Document

import datetime

from app.db.schemas import GenericResponseModel, EvidenceDataInputModel
from app.utils.common import get_unique_id, get_current_time, error_return, success_return
from pydantic import  Field


class BaseDocument(Document):

    @classmethod
    async def get_page(cls, query=None, options={"page": 1, "pagesize": 10, "sort": {"_id": -1}}, callback=None,
                       is_async_callback=False):
        if query is None:
            query = {}
        if options['page'] < 1:
            options['page'] = 1
        if options['pagesize'] < 10:
            options['pagesize'] = 10

        skip = (options['page'] - 1) * options['pagesize']
        limit = options['pagesize']
        sort = options['sort']

        total = await cls.find(query).count()
        total_page = math.ceil(total / options['pagesize'])

        objects = await cls.find(query).sort(sort).skip(skip).limit(limit).to_list()
        if callback is not None:
            if is_async_callback:
                objects = await asyncio.gather(*[callback(obj) for obj in objects])
            else:
                objects = list(map(callback, objects))

        out = {
            "total": total,
            "total_page": total_page,
            "list": objects
        }
        return GenericResponseModel(result=out)


class EvidenceData(BaseDocument):
    id: str = Field(default_factory=get_unique_id)
    task_id: str
    node_id:str=""
    data_hash: str
    raw_data: str = ""
    transaction_hash: str = ""
    data:Any
    status: int = 0
    create_at: int = get_current_time()
    update_at: int = get_current_time()

    class Settings:
        name = "evidence_data"

    @classmethod
    async def try_add_evidence(cls,form:EvidenceDataInputModel):
        try:
            data_hash = sha256(form.data.encode()).hexdigest()

            evidence = await cls.find_one({"task_id":form.task_id})
            if evidence is not None:
                return error_return(code=1, message="task_id exists")
            decoded_bytes = base64.b64decode(form.data)
            decoded_str = decoded_bytes.decode('utf-8')
            data = json.loads(decoded_str)
            doc = {
                "data_hash": data_hash,  #
                "raw_data": form.data,
                "task_id": form.task_id,
                "data": data,
                "node_id":form.node_id
            }
            evidence = await EvidenceData(**doc).create()

            return success_return({"task_id": evidence.task_id,"data_hash": evidence.data_hash,"node_id":form.node_id})

        except Exception as e:
            print(e)
            return error_return(code=500, message="data error",data=form)

    @classmethod
    async def update_task_hash(cls,task_id,hash):
        return await cls.find_one({"task_id":task_id}).update_one({"$set":{"transaction_hash":hash,"status":1,"update_at":get_current_time()}})
