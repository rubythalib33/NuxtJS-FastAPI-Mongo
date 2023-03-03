from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class Admin(Document):
    fullname: str
    email: EmailStr
    password: str
    role: str = "admin"

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
                "role": "admin"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "abdul@youngest.dev",
                "password": "3xt3m#",
            }
        }


class AdminData(BaseModel):
    fullname: str
    email: EmailStr
    role: str = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "role": "admin"
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }