from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.schemas.dashboard import HomeDashboardResponse
from app.services.store import store


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/home", response_model=HomeDashboardResponse)
def home_dashboard(user: dict = Depends(get_current_user)) -> dict:
    return store.dashboard_home(user_id=user["id"])
