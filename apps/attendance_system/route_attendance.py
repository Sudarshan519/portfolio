from fastapi import APIRouter
 
from . import route_index
attendance_router = APIRouter(include_in_schema=True)
attendance_router.include_router(route_index.router, prefix="/attendance", tags=[ ])