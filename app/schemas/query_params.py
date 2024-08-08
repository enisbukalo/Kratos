from dataclasses import dataclass

from pydantic import ConfigDict
from fastapi import Query


@dataclass
class GetQueryParams:
    page_size: int = Query(default=100, gt=0, le=1001)
    page_number: int = Query(default=1, gt=0)
    sort: bool = Query(default=False)

    model_config = ConfigDict(from_attributes=True)
