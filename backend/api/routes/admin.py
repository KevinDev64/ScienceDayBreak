from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import async_get_db
from core.constants import require_admin
from database import User, Role

router = APIRouter(prefix="/admin", tags=["Авторизация"])


@router.patch("/users/{user_id}/role")
async def change_user_role(
        user_id: int,
        new_role: Role,
        db: AsyncSession = Depends(async_get_db),
        admin: User = Depends(require_admin)
):
    """Изменение роли"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.role = new_role
    await db.commit()
    return {"message": f"Роль изменена на {new_role.value}"}
