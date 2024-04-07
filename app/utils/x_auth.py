import os

from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status

load_dotenv()

#Just For POC,will refactor
x_auth_header_key = os.getenv("X_AUTH_KEY")

#  simple X-Auth Header
api_key_header = APIKeyHeader(name="X-Auth", auto_error=False)


async def check_auth(x_auth: str = Depends(api_key_header)):
    if x_auth is not None:
        if x_auth == x_auth_header_key:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Auth Header",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Auth Header",
        )

