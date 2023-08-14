from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger as loguru_logger
from app.schemas.response_schema import ResponseBody
from app.schemas.password_reset_schema import RequestBody

router = APIRouter(
    prefix="/password",
    tags=["password-reset"]
)

@router.post("/reset-request", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def reset_password(request_data: RequestBody) -> ResponseBody:
    # TODO check if user exists
    

    # TODO generate refresh token
    # TODO save refresh token to database
    # TODO send email to requesting email address
    # TODO
    # TODO
    # TODO
    # TODO