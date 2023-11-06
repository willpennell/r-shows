from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.user_schemas import UserRegistrationRequest, UserUpdateRequest, UserPartialUpdateRequest
from app.services.user_service import UserService
from app.schemas.response_schema import ResponseBody
from app.schemas.activation_token_schema import RequestBody as ActivationRequest
from app.db.activation_token_repository import ActivationTokenRepository
from app.services.email_service import EmailService
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from loguru import logger as log
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService


from app.db.user_repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseBody)
def register_user(request_data: UserRegistrationRequest, db: Session = Depends(get_db)) -> ResponseBody:
    user_repository = UserRepository(db)
    activation_repository = ActivationTokenRepository(db)
    user_service = UserService(user_repository, activation_repository, EmailService())
    log.info("Can Post")
    try:
        user = user_service.create_user(request_data)
        
        if user.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
            
        response = ResponseBody(
            success=True,
            response={"user_id": user.id},
            message="User successfully created."
        )
        return response

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user())) -> ResponseBody:
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        
        log.info("In user_router")
        user = user_service.get_user(user_id)
        
        if not user.active:
            raise HTTPException(
                status_code=403,
                detail="Account not active"
            )
        
        if not user.active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not active"
                )
        
        response = ResponseBody(
                success=True,
                response=user.__dict__,
                message="User successfully retrieved."
            )
        return response
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def update_user_by_id(user_id: int, updated_user_data: UserUpdateRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> ResponseBody:
    try:
        log.info("user_router - update user (PUT)")
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        
        existing_user = user_service.get_user(user_id)
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
            
        if not existing_user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not active"
            )
        
        updated_user = user_service.update_user(user_id, updated_user_data)
    
        response = ResponseBody(
            success=True,
            response=updated_user.__dict__,
            message="User successfully updated."
        )

        return response
    except ValueError as ve:
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve) 
            )
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )

@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def partial_update_user_by_id(user_id: int, updated_user_data: UserPartialUpdateRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> ResponseBody:
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        
        user = user_service.get_user(user_id)
        
        if not user or user.deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not active"
            )
            
            
        updated_user = user_service.partial_update_user(user_id, updated_user_data)
        
        if not updated_user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not active"
            )

        response = ResponseBody(
            success=True,
            response=updated_user.__dict__,
            message="User successfully updated."
        )

        return response
    except ValueError as ve:
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve) 
            )
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )

@router.get("/account/activate", status_code=status.HTTP_204_NO_CONTENT)
def activate_user(token: str = Query(...), db: Session = Depends(get_db)):
    try: 
        user_repository = UserRepository(db)
        activation_repository = ActivationTokenRepository(db)
        email_service = EmailService()
        user_service = UserService(user_repository, activation_repository, email_service)
        
        user_service.activate_user(token)
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )

@router.post("/account/resend-activation", status_code=status.HTTP_204_NO_CONTENT)
def resend_activation_token(request_body: ActivationRequest, db: Session = Depends(get_db)):
    try: 
        user_repository = UserRepository(db)
        activation_repository = ActivationTokenRepository(db)
        email_service = EmailService()
        user_service = UserService(user_repository, activation_repository, email_service)
        
        user = user_service.get_user_by_email(request_body.email)
        if not user or user.deleted:
            raise HTTPException(status_code=404, detail="User not found")
        if user.active:
            raise HTTPException(status_code=400, detail="USer already activate")

        user_service.resend_activation(user)
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )
        
@router.get("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_account(user_id: int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try: 
        user_repository = UserRepository(db)
        activation_repository = ActivationTokenRepository(db)
        email_service = EmailService()
        user_service = UserService(user_repository, activation_repository, email_service)
        
        user = user_service.get_user(user_id)
        if not user or user.deleted:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.active:
            raise HTTPException(status_code=403, detail="User not active")
        
        user_service.deactivate_user(user)
        
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )

@router.delete("/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try: 
        user_repository = UserRepository(db)
        activation_repository = ActivationTokenRepository(db)
        email_service = EmailService()
        user_service = UserService(user_repository, activation_repository, email_service)
        
        user = user_service.get_user(user_id)
        if not user or user.deleted:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.active:
            raise HTTPException(status_code=403, detail="User not active")
        
        user_service.delete_user(user)
        
    except OperationalError:
        raise HTTPException(
            status_code=500,
            detail="Internal Error"
        )
        

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        auth_service = AuthService()
        user_data = auth_service.validate_token(token)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
