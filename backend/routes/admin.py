from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext


from database.database import add_admin, retrieve_admins
from models.admin import Admin, AdminData, Response

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.get("/", response_description="Admin retrieved", response_model=Response)
async def get_admin():
    admins = await retrieve_admins()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Admin data retrieved successfully",
        "data": admins
    }


@router.post("/new", response_model=AdminData)
async def admin_signup(admin: Admin = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin.email)
    if admin_exists:
        raise HTTPException(
            status_code=409,
            detail="Admin with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(admin)
    return new_admin
