from fastapi import APIRouter, FastAPI
from .employee import route_employee 
from .employer import route_employer
from .approver import route_approver
from . import route_base
attendance_router =FastAPI(title="HAJIR APP API AND BACKEND",description="Visit routes for all apis")# APIRouter(include_in_schema=True)
# attendance_router.include_router(route_base.router, prefix="/attendance", tags=[ ])
attendance_router.include_router(route_employer.router,prefix='/employer')
attendance_router.include_router(route_approver.router,prefix='/approver')
attendance_router.include_router(route_employee.router,prefix='/employee')