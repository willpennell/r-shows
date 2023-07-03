from fastapi import APIRouter
from app.schemas.user_schemas import UserRegistrationRequest
from app.schemas.response_schema import ResponseBody

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", status_code=201)
async def register_user(user_data: UserRegistrationRequest):
    
    response = ResponseBody(
        success=True,
        response={"user_id": 1},
        message="User successfully created."
    )

    return response