from typing import Optional
from pydantic import BaseModel, Field


class Response(BaseModel):
    """
    Response - Simple response containing a message.

        message: The message of this JobsDelete201Response [Optional].
    """

    message: Optional[str] = Field(alias="message", default=None)


Response.update_forward_refs()
