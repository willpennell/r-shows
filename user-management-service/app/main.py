from fastapi import FastAPI
from app.routers.user_router import router as user_router
from app.routers.password_reset_router import router as password_token_router
from loguru import logger as loguru_logger


app = FastAPI(debug=True)

@app.on_event("startup")
async def startup_event():
    loguru_logger.add("app.log", rotation="500 MB", level="DEBUG")  # Define log file and rotation
    

app.include_router(user_router)
app.include_router(password_token_router)
