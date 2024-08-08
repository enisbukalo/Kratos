from pydantic import BaseModel, ConfigDict, Field

from .query_params import GetQueryParams


class BoneBase(BaseModel):
    id: int
    name: str
    length_cm: float
    skeleton_id: int
    skeleton: "Skeleton"


class Bone(BoneBase):
    model_config = ConfigDict(from_attributes=True)


class CreateBone(BaseModel):
    name: str = Field(default="Bone Name", min_length=4, max_length=100)
    length_cm: float = Field(default=65.89, gt=0)
    skeleton_id: int


class BonesQuery(GetQueryParams):
    pass


from .skeleton import Skeleton

BoneBase.model_rebuild()
