from typing import Union

from pydantic import BaseModel, Field


class Filter(BaseModel):
    """
    Metadata filter for retrieving jobs. Only exact matches with string or integer values are supported.
    """

    key: str = Field(alias="key", description="Metadata key name.")
    value: Union[str, int] = Field(alias="value", description="Metadata value.")


Filter.update_forward_refs()
