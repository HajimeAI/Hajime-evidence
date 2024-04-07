import asyncio
from asyncio import sleep

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.db.models import EvidenceData
from app.db.schemas import EvidenceDataInputModel, GenericResponseModel
from app.service.solana_service import SolanaService
from app.utils.x_auth import check_auth

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custome Excpeption Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=200,
        content={"code": exc.status_code, "message": exc.detail}
    )


async def execute_periodic_function():
    """
    TODO: Check failed task
    :return:
    """
    pass


scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def app_start():
    scheduler.add_job(execute_periodic_function, 'interval', seconds=30)
    scheduler.start()
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


async def save_hash_to_blockchain(task_id: str, data_hash: str,node_id:str):
    transaction_hash = await SolanaService.call_evidence_contract(data_hash)
    print("task_id,block_hash:",task_id, transaction_hash)
    if transaction_hash != "":
        await EvidenceData.update_task_hash(task_id, transaction_hash)
        await SolanaService.callback(node_id,transaction_hash)



async def background_task(task_id, data_hash,node_id):
    asyncio.create_task(save_hash_to_blockchain(task_id, data_hash,node_id))
@app.post("/hash_to_blockchain", response_model=GenericResponseModel, summary="data hash to blockchain")
async def hash_to_blockchain(form: EvidenceDataInputModel,
                             background_tasks: BackgroundTasks,
                             auth: bool = Depends(check_auth),
                             ):
    ret = await EvidenceData.try_add_evidence(form)
    if ret.code == 0:
        background_tasks.add_task(background_task, ret.result['task_id'], ret.result['data_hash'],ret.result['node_id'])
    return ret


@app.get("/ping")
def ping():
    return GenericResponseModel()
