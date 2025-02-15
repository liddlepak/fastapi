from src.repositories.base import BaseRepositories
from src.models.facilities import FacilitiesModel, RoomFacilitiesModel
from src.repositories.mappers.mappers import FacilityMapper
from src.schemas.facilities import RoomsFacilities, RoomsFacilitiesAdd


class FacilitiesRepositories(BaseRepositories):
    """Репозиторий удобств."""
    model = FacilitiesModel
    mapper = FacilityMapper


class RoomsFacilitiesRepositories(BaseRepositories):
    """Репозиторий номера с удобствами."""
    model = RoomFacilitiesModel
    schema = RoomsFacilities

    async def edit_facility(self, request_ids, room_id):
        """Редактирование удобств в номере."""
        room_facility = await self.get_filtred(room_id=room_id)
        facilities_ids = [
            item.model_dump()["facility_id"] for item in room_facility]
        if request_ids is None:
            await self.delete_bulk(facilities_ids)
            return {"success delete"}
        delete_ids = set(facilities_ids).difference(set(request_ids))
        add_ids = set(request_ids).difference(set(facilities_ids))
        if add_ids:
            update_facilities = [RoomsFacilitiesAdd(
                room_id=room_id, facility_id=id) for id in add_ids]
            await self.add_bulk(update_facilities)
        if delete_ids:
            await self.delete_bulk(delete_ids)
