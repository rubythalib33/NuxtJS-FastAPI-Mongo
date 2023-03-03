from auth.jwt_handler import sign_jwt
from models.admin import Admin, AdminSignIn
from fastapi import APIRouter, Body, HTTPException
from passlib.context import CryptContext

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    if admin_exists:
        password = hash_helper.verify(
            admin_credentials.password, admin_exists.password)
        if password:
            # return admin role
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Admin logged in successfully",
                "data": {
                    "role": admin_exists.role,
                    "token": sign_jwt(admin_exists.email)
                }
            }

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )

    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )