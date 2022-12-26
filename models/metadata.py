from typing import List, Optional
from pydantic import BaseModel, Field

class Metadata(BaseModel):
    """
    Metadata - a model defined in OpenAPI

        status: The status of this Metadata [Optional].
        encode_status: The encode_status of this Metadata [Optional].
        artifacts: The artifacts of this Metadata [Optional].
    """

    status: Optional[str] = Field(alias="status", default=None)
    encode_status: Optional[List[str]] = Field(alias="encode_status", default=None)
    artifacts: Optional[List[str]] = Field(alias="artifacts", default=None)

Metadata.update_forward_refs()
