from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator
from models.header import Header


class Upload(BaseModel):
    """
    Specifies where transcoded video should be uploaded.
    """

    url_list: List[str] = Field(
        alias="url_list", description="List of URLs where video data will be uploaded."
    )
    chunk_size: int = Field(
        alias="chunk_size", description="Maximum chunk size for each URL in bytes."
    )
    header_list: Optional[List[Header]] = Field(
        alias="header_list",
        default=None,
        description="Header values that should be used in each request.",
    )

    @validator("chunk_size")
    def chunk_size_min(cls, value):
        assert value >= 0
        return value


Upload.update_forward_refs()
