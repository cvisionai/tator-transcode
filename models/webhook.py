from typing import List, Optional
from pydantic import BaseModel, Field
from models.header import Header

class Webhook(BaseModel):
    """
    Webhook - a model defined in OpenAPI

        url: The url of this Webhook.
        method: The method of this Webhook.
        stage: The stage of this Webhook.
        header_list: The header_list of this Webhook [Optional].
    """

    url: str = Field(alias="url")
    method: str = Field(alias="method")
    stage: str = Field(alias="stage")
    header_list: Optional[List[Header]] = Field(alias="header_list", default=None)

Webhook.update_forward_refs()
