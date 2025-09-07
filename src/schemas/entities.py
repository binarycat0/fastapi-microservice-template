from pydantic import BaseModel, Field

from db.models.entity import Entity


class GenerateEntitiesModel(BaseModel):
    count: int = Field(default=1)
    type: Entity.Type = Field(default=Entity.Type.DUMMY)
