from typing import Union

from pydantic import BaseModel, Field

class Filter(BaseModel):
    """
    Filter - a model defined in OpenAPI

        key: The key of this Filter.
        value: The value of this Filter.
    """

    key: str = Field(alias="key")
    value: Union[str, int] = Field(alias="value")

Filter.update_forward_refs()
