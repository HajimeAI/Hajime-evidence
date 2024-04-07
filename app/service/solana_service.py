import os

from dotenv import load_dotenv
import httpx
from solana.rpc.api import Client
from solders.instruction import Instruction, AccountMeta
import solana.transaction as txlib

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from solana.transaction import Transaction
import json

load_dotenv()
program_id_str = os.getenv("PROGRAM_ID")
solana_rpc_url = os.getenv("SOLANA_RPC_URL")
key_file = os.getenv("KEY_FILE")
callback_url = os.getenv("HASH_TO_BLOCKCHAIN_CALLBACK")

secret = None
with open(key_file, 'r') as file:
    secret = json.load(file)

x_auth_header_key = os.getenv("X_AUTH_KEY")


class SolanaService:

    @classmethod
    async def call_evidence_contract(cls, data: str):
        """
        TODO:Add Exception Check and Retry Logical
        :param data:
        :return:
        """
        client = AsyncClient(solana_rpc_url)
        await client.is_connected()
        keys = bytes(secret)

        sender = Keypair.from_bytes(keys)
        program_id = Pubkey.from_string(program_id_str)
        account = AccountMeta(pubkey=sender.pubkey(), is_signer=True, is_writable=True)
        hash_bytes = bytes(data, 'utf-8')
        tx = txlib.Instruction(
            program_id=program_id,
            data=hash_bytes,
            accounts=[account],
        )

        transaction_hash = ""
        try:
            txn = Transaction().add(tx)
            response = await client.send_transaction(txn, sender)
            confirmation = await client.confirm_transaction(response.value)
            # print(response)
            transaction_hash = str(response.value)
        except Exception as e:
            print(e)
        return transaction_hash


    @classmethod
    async def callback(cls, node_id,transaction_hash):
        """
        TODO:add response check
        :param node_id:
        :param transaction_hash:
        :return:
        """
        custom_headers = {
            'X-Auth': x_auth_header_key,
            'Content-Type':'application/json'
        }
        doc = {
            "kind": "evidence",
            "node_id": node_id,
            "content": {
                "text": transaction_hash
            }
        }
        async with httpx.AsyncClient() as aclient:
            response = await aclient.post(
                callback_url,
                json=doc,
                headers=custom_headers
            )
            print(response)
