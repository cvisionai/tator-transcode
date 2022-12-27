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
    size: Optional[int] = Field(alias="size", default=None, description="Size of the file in bytes. Required when the given URL does not accept HEAD requests.")
    header_list: Optional[List[Header]] = Field(alias="header_list", default=None, description="List of headers used for download requests on the source video file.")
    encode_list: List[Encode] = Field(alias="encode_list", description="List of encode settings, one per output file.")
    metadata: Optional[Metadata] = Field(alias="metadata", default=None)

Job.update_forward_refs()
