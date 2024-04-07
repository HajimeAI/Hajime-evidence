from hashlib import sha256

from solana.rpc.api import Client
from solders.instruction import Instruction, AccountMeta
import solana.transaction as txlib

http_client = Client("https://api.devnet.solana.com")
import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from solana.transaction import Transaction


async def main():
    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    # fill your keys
    keys = bytes(

        )

    sender = Keypair.from_bytes(keys)
    print(sender.pubkey())

    program_id = Pubkey.from_string("HVywFTz6QmtxviYPFH14WehvFvs5BhWDbgKz2ec7WSEK")
    print(program_id)
    account = AccountMeta(pubkey=sender.pubkey(), is_signer=True, is_writable=True)

    data = "hajime is coming"
    data_hash = sha256(data.encode()).hexdigest()
    arr = bytes(data_hash, 'utf-8')
    tx = txlib.Instruction(
        program_id=program_id,
        data=arr,
        accounts=[account],
    )
    txn = Transaction().add(tx)
    response = await client.send_transaction(txn, sender)

    confirmation = await  client.confirm_transaction(response.value)
    print(response)
    print(confirmation)

    await client.close()


asyncio.run(main())
