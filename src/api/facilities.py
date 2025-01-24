from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Список удобств")
@cache(expire=30)
async def get_facilities(db: DBDep) -> list:
    """Получение списка всех удобств."""
    return await db.facilities.get_filtred()


@router.post("", summary="Добавление удобств")
async def add_facilities(db: DBDep, data: FacilitiesRequest) -> dict:
    """Функиция для добавление удобства."""
    facility = await db.facilities.add(data=data)
    await db.commit()
    return {"facility": facility}
