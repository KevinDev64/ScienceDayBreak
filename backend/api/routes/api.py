from fastapi import APIRouter

from api.routes import user, auth, operator, admin
router = APIRouter(prefix="/v1")
router.include_router(user.router)
router.include_router(operator.router)
router.include_router(auth.router)
router.include_router(admin.router)