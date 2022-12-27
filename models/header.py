from typing import Union

from pydantic import BaseModel, Field


class Header(BaseModel):
    """
    Header name and value used in a request.
    """

    name: str = Field(alias="name", description="Name of the header.")
    value: Union[str, int] = Field(alias="value", description="Value of the header.")


Header.update_forward_refs()
