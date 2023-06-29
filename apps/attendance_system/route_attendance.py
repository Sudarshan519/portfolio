from fastapi import APIRouter
from .employee import route_employee 
from .employer import route_employer
from . import route_base
attendance_router = APIRouter(include_in_schema=True)
# attendance_router.include_router(route_base.router, prefix="/attendance", tags=[ ])
attendance_router.include_router(route_employee.router,prefix='/employee')
attendance_router.include_router(route_employer.router,prefix='/employer')