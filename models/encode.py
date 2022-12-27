from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from .upload import Upload
from .webhook import Webhook


class Encode(BaseModel):
    """
    Encode settings for one output file.
    """

    codec: str = Field(
        alias="codec",
        description="Codec. If an audio codec is selected, an audio stream will be used as input from the file.",
    )
    width: int = Field(alias="width", description="Width in pixels.")
    height: int = Field(alias="height", description="Height in pixels.")
    rate: Optional[float] = Field(
        alias="rate", default=None, description="Frame rate in frames per second."
    )
    settings: Optional[Dict[str, Union[str, int, float]]] = Field(
        alias="settings",
        default=None,
        description="Other settings for the encode. May include stream selectors, presets, crf, etc.",
    )
    upload_list: List[Upload] = Field(
        alias="upload_list", description="List of uploads for completed file."
    )
    webhook_list: Optional[List[Webhook]] = Field(
        alias="webhook_list",
        default=None,
        description="List of webhooks for this encode.",
    )

    @validator("codec")
    def codec_enum(cls, value):
        assert value.lower() in ["avc", "hevc", "av1", "aac", "copy"]
        return value.lower()

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
