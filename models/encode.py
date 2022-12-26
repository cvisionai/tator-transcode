from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from .upload import Upload
from .webhook import Webhook

class Encode(BaseModel):
    """
    Encode - a model defined in OpenAPI

        codec: The codec of this Encode.
        width: The width of this Encode.
        height: The height of this Encode.
        rate: The rate of this Encode [Optional].
        settings: The settings of this Encode [Optional].
        upload_list: The upload_list of this Encode.
        webhook_list: The webhook_list of this Encode [Optional].
    """

    codec: str = Field(alias="codec")
    width: int = Field(alias="width")
    height: int = Field(alias="height")
    rate: Optional[float] = Field(alias="rate", default=None)
    settings: Optional[Dict[str, Union[str, int, float]]] = Field(alias="settings", default=None)
    upload_list: List[Upload] = Field(alias="upload_list")
    webhook_list: Optional[List[Webhook]] = Field(alias="webhook_list", default=None)

    @validator("width")
    def width_min(cls, value):
        assert value >= 1
        return value

    @validator("height")
    def height_min(cls, value):
        assert value >= 1
        return value

    @validator("rate")
    def rate_min(cls, value):
        assert value >= 0
        return value

Encode.update_forward_refs()
