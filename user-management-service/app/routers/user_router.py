from fastapi import APIRouter, Depends

from app.schemas.user_schemas import UserRegistrationRequest
from app.services.user_service import UserService
from app.schemas.response_schema import ResponseBody
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)



@router.post("/register", status_code=201)
async def register_user(request_data: UserRegistrationRequest, db=Depends(get_db)):
    user_service = UserService(db)
    user = user_service.create_user(request_data)

    response = ResponseBody(
        success=True,
        response={"user_id": user.id},
        message="User successfully created."
    )

    return response