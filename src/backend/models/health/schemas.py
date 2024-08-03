from pydantic import BaseModel

class HealthReponse(BaseModel):
    alive: bool = True

class ErrorResponse(BaseModel):
    detail: str