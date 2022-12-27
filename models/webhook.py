from typing import List, Optional
from pydantic import BaseModel, Field, validator
from models.header import Header


class Webhook(BaseModel):
    """
    Specifies a request that should be made during transcode.
    """

    url: str = Field(alias="url", description="URL where request should be sent.")
    method: str = Field(
        alias="method", description="HTTP method that should be used for the request."
    )
    stage: str = Field(
        alias="stage", description="When the webhook should be triggered."
    )
    header_list: Optional[List[Header]] = Field(
        alias="header_list",
        default=None,
        description="List of headers that should be included with the request.",
    )

    @validator("method")
    def method_enum(cls, value):
        assert value.upper() in ["POST", "PUT", "GET", "OPTIONS", "DELETE"]
        return value.upper()

    @validator("stage")
    def stage_enum(cls, value):
        assert value.lower() in ["start", "progress", "completion"]
        return value.lower()


Webhook.update_forward_refs()
