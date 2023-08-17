from fastapi import APIRouter, Depends, HTTPException, status, Query
from loguru import logger as loguru_logger
from app.schemas.response_schema import ResponseBody
from app.schemas.password_reset_schema import RequestBody
from app.services.password_service import PasswordService
from app.db.password_token_repository import PasswordTokenRepository
from app.db.user_repository import UserRepository
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.email_service import EmailService
from loguru import logger as loguru_logger

router = APIRouter(
    prefix="/password",
    tags=["password"]
)

@router.post("/reset-request", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(request_data: RequestBody, db: Session = Depends(get_db)):
    password_token_repository = PasswordTokenRepository(db)
    user_repository = UserRepository(db)
    password_service = PasswordService(password_token_repository, user_repository)
    
    loguru_logger.info("calling generate token")
    password_service.generate_token(request_data.email)

@router.get("/confirm", status_code=status.HTTP_200_OK)
def confirm_reset(token: str = Query(...), db: Session = Depends(get_db)):
    password_token_repository = PasswordTokenRepository(db)
    user_repository = UserRepository(db)
    password_service = PasswordService(password_token_repository, user_repository)
    if password_service.verify_reset_token(token):
        return {"message": "Token is valid. You can now reset your password."}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")