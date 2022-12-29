from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from models.metadata import Metadata


class Job(BaseModel):
    """
    Represents workload associated with one input file.
    """

    url: str = Field(alias="url", description="URL where source video file is hosted.")
    host: str = Field(alias="host", description="Tator host URL.")
    token: str = Field(alias="token", description="Tator API token.")
    project: int = Field(
        alias="project", description="Unique integer specifying project ID."
    )
    type: int = Field(
        alias="type", description="Unique integer specifying a media type."
    )
    name: str = Field(alias="name", description="Name of the video file.")
    section: str = Field(alias="section", description="Media section name.")
    attributes: Optional[Dict[str, Any]] = Field(
        alias="attributes", description="Attributes to set on the media."
    )
    media_id: Optional[int] = Field(
        alias="media_id", description="Media ID.", default=-1
    )
    gid: Optional[str] = Field(alias="gid", description="Upload group ID.")
    uid: Optional[str] = Field(alias="uid", description="Upload unique ID.")
    group_to: Optional[int] = Field(
        alias="group_to",
        default=1080,
        description="Vertical resolutions below this will be transcoded with "
        "multi-headed ffmpeg.",
    )
    status: Optional[str] = Field(
        alias="status",
        default=None,
        description="Overall status of the job. Set by the service (ignored on job creation).",
    )

    @validator("status")
    def status_enum(cls, value):
        assert value.lower() in ["pending", "running", "succeeded", "failed"]
        return value.lower()


Job.update_forward_refs()
