from typing import Optional, Any


class DataMapper:
    """Паттерн DataMapper."""
    db_model: Optional[Any] = None
    schema: Optional[Any] = None

    @classmethod
    def map_to_domain_entity(self, data):
        return self.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistense_entity(self, data):
        return self.db_model(**data.model_dump())
