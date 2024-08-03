from fastapi import APIRouter, Depends, HTTPException, status
from models.health.schemas import HealthReponse, ErrorResponse

router = APIRouter(prefix="/api", tags=['health'])


@router.get('/health', description="Get health status",
           responses={
               status.HTTP_200_OK : {"model": HealthReponse},
               status.HTTP_400_BAD_REQUEST : {"model": ErrorResponse},
           })
async def health():
    return HealthReponse(alive=True)