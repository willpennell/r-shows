from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import UserRegistrationRequest, UserUpdateRequest, UserPartialUpdateRequest
from app.services.user_service import UserService
from app.schemas.response_schema import ResponseBody
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from loguru import logger as loguru_logger


from app.db.user_repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseBody)
def register_user(request_data: UserRegistrationRequest, db: Session = Depends(get_db)) -> ResponseBody:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    loguru_logger.info("Can Post")
    try:
        user = user_service.create_user(request_data)
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

    


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def get_user_by_id(user_id, db: Session = Depends(get_db)) -> ResponseBody:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    loguru_logger.info("In user_router")
    user = user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")
    
    response = ResponseBody(
            success=True,
            response=user.__dict__,
            message="User successfully retrieved."
        )
    return response


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def update_user_by_id(user_id: int, updated_user_data: UserUpdateRequest, db: Session = Depends(get_db)) -> ResponseBody:
    try:
        loguru_logger.info("user_router - update user (PUT)")
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        
        existing_user = user_service.get_user(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
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

@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseBody)
def partial_update_user_by_id(user_id: int, updated_user_data: UserPartialUpdateRequest, db: Session = Depends(get_db)) -> ResponseBody:
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)

        
        
        existing_user = user_service.get_user(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        updated_user = user_service.partial_update_user(user_id, updated_user_data)

        
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