from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Список удобств")
async def get_facilities(db: DBDep):
    return await db.facilities.get_filtred()


@router.post("", summary="Добавление удобств")
async def add_facilities(db: DBDep, data: FacilitiesRequest):
    facility = await db.facilities.add(data=data)
    await db.commit()
    return {"facility": facility}
