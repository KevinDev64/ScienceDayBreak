from fastapi import APIRouter

from api.routes import user, auth

router = APIRouter(prefix="/v1")
router.include_router(user.router)
router.include_router(auth.router)
