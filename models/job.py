from typing import List, Optional
from pydantic import BaseModel, Field
from models.encode import Encode
from models.header import Header
from models.metadata import Metadata


class Job(BaseModel):
    """
    Represents workload associated with one input file.
    """

    url: str = Field(alias="url", description="URL where source video file is hosted.")
    name: str = Field(alias="name", description="Name of the video file.")
    size: int = Field(
        alias="size",
        description="Size of the file in bytes.",
    )
    header_list: Optional[List[Header]] = Field(
        alias="header_list",
        default=None,
        description="List of headers used for download requests on the source video file.",
    )
    encode_list: List[Encode] = Field(
        alias="encode_list", description="List of encode settings, one per output file."
    )
    metadata: Optional[Metadata] = Field(alias="metadata", default=None)

    @validator("size")
    def size_min(cls, value):
        assert value >= 1
        return value


Job.update_forward_refs()
