from fastapi import APIRouter
 
from . import route_index
webapp_router = APIRouter()
webapp_router.include_router(route_index.router, prefix="", tags=["job-webapp"])