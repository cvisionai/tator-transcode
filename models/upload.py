from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator
from models.header import Header


class Upload(BaseModel):
    """
    Upload - a model defined in OpenAPI

        url_list: The url_list of this Upload.
        chunk_size: The chunk_size of this Upload.
        header_list: The header_list of this Upload [Optional].
    """

    url_list: List[str] = Field(alias="url_list")
    chunk_size: int = Field(alias="chunk_size")
    header_list: Optional[List[Header]] = Field(alias="header_list", default=None)

    @validator("chunk_size")
    def chunk_size_min(cls, value):
        assert value >= 0
        return value


Upload.update_forward_refs()
