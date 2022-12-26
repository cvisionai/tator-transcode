from typing import List, Optional
from pydantic import BaseModel, Field
from models.encode import Encode
from models.header import Header
from models.metadata import Metadata

class Job(BaseModel):
    """
    Job - a model defined in OpenAPI

        url: The url of this Job.
        header_list: The header_list of this Job [Optional].
        encode_list: The encode_list of this Job.
        metadata: The metadata of this Job [Optional].
    """

    url: str = Field(alias="url")
    header_list: Optional[List[Header]] = Field(alias="header_list", default=None)
    encode_list: List[Encode] = Field(alias="encode_list")
    metadata: Optional[Metadata] = Field(alias="metadata", default=None)

Job.update_forward_refs()
