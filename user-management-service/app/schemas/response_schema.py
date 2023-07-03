from pydantic import BaseModel
from typing import Dict, Any

class ResponseBody(BaseModel):
    success: bool
    response: Dict[str, Any]
    message: str