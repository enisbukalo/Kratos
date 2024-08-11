from pydantic import BaseModel, ConfigDict, Field

from .query_params import GetQueryParams


class SkeletonBase(BaseModel):
    id: int
    name: str
    height_m: float


class Skeleton(SkeletonBase):
    model_config = ConfigDict(from_attributes=True)


class CreateSkeleton(BaseModel):
    name: str = Field(default="Bone Name", min_length=4, max_length=100)
    height_m: float = Field(default=1.97, gt=0)


class SkeletonsQuery(GetQueryParams):
    pass


from .bone import Bone

Bone.model_rebuild()
