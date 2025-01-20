from fastapi import HTTPException, Security, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

security = HTTPBasic()


async def get_current_username(credentials: HTTPBasicCredentials = Security(security)):
    correct_username = os.getenv("SWAGGER_USERNAME")
    correct_password = os.getenv("SWAGGER_PASSWORD")
    try:
        if (
            credentials.username == correct_username
            and credentials.password == correct_password
        ):
            return credentials.username
    except HTTPException as e:
        return Response(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return Response(status_code=500, content={"detail": "Internal Server Error"})
