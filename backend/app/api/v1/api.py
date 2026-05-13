from fastapi import APIRouter
from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.devices import router as devices_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.practice import router as practice_router
from app.api.v1.endpoints.questions import router as questions_router
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(devices_router)
api_router.include_router(practice_router)
api_router.include_router(questions_router)
api_router.include_router(analytics_router)
api_router.include_router(dashboard_router)
api_router.include_router(notifications_router)
