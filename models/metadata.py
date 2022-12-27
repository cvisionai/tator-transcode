from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, validator


class Metadata(BaseModel):
    """
    Optional descriptors for a job.
    """

    status: Optional[str] = Field(
        alias="status",
        default=None,
        description="Overall status of the job. Set by the service (ignored on job creation).",
    )
    encode_status: Optional[List[str]] = Field(
        alias="encode_status",
        default=None,
        description="Status of individual encodes. Set by the service (ignored on job creation).",
    )
    artifacts: Optional[Dict[str, Union[str, int]]] = Field(
        alias="artifacts",
        default=None,
        description="List of locations of job artifacts. Set by the service (ignored on job creation).",
    )

    @validator("status")
    def status_enum(cls, value):
        assert value.lower() in ["pending", "running", "succeeded", "failed"]
        return value.lower()

    @validator("encode_status")
    def encode_status_enum(cls, value):
        for item in value:
            assert item.lower() in ["pending", "running", "succeeded", "failed"]
        return [item.lower() for item in value]


Metadata.update_forward_refs()
