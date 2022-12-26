from typing import Union

from pydantic import BaseModel, Field


class Header(BaseModel):
    """
    Header - a model defined in OpenAPI

        name: The name of this Header.
        value: The value of this Header.
    """

    name: str = Field(alias="name")
    value: Union[str, int] = Field(alias="value")

Header.update_forward_refs()
