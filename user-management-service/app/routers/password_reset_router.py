from fastapi import APIRouter, Depends, HTTPException, status, Query
from loguru import logger as loguru_logger
from app.schemas.response_schema import ResponseBody
from app.schemas.password_reset_schema import RequestBody, UpdatePasswordRequest
from app.services.password_service import PasswordService
from app.services.user_service import UserService
from app.db.password_token_repository import PasswordTokenRepository
from app.db.user_repository import UserRepository
from app.database import get_db
from sqlalchemy.orm import Session
from loguru import logger as log
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/password",
    tags=["password"]
)

@router.post("/reset-request", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(request_data: RequestBody, db: Session = Depends(get_db)):
    try:
        password_token_repository = PasswordTokenRepository(db)
        user_repository = UserRepository(db)
        password_service = PasswordService(password_token_repository, user_repository)
    
        log.info("calling generate token")
        password_service.generate_token(request_data.email)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid email")
        

@router.get("/confirm", status_code=status.HTTP_200_OK)
def confirm_reset(token: str = Query(...), db: Session = Depends(get_db)):
    password_token_repository = PasswordTokenRepository(db)
    user_repository = UserRepository(db)
    password_service = PasswordService(password_token_repository, user_repository)
    if password_service.verify_reset_token(token):
        return {"message": "Token is valid. You can now reset your password."}
    else:
        raise HTTPException(status_code=400, detail="Invalid token")
    

@router.post("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_password(update_password_request: UpdatePasswordRequest, db: Session = Depends(get_db)):
    password_token_repository = PasswordTokenRepository(db)
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    password_service = PasswordService(password_token_repository, user_repository)
    
    log.info("in update router")
    if password_service.verify_reset_token(update_password_request.token):
        log.info("in if block passed verification")
        user_service.update_user_password(update_password_request.email, update_password_request.new_password)
