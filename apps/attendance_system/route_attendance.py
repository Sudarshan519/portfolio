from fastapi import APIRouter
 
from . import route_base
attendance_router = APIRouter(include_in_schema=True)
attendance_router.include_router(route_base.router, prefix="/attendance", tags=[ ])