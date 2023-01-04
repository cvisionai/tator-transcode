from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from dateutil.parser import parse


class Job(BaseModel):
    """
    Represents workload associated with one input file.
    """

    url: str = Field(alias="url", description="URL where source video file is hosted.")
    size: int = Field(alias="size", description="Size of the video file in bytes.")
    md5: str = Field(alias="md5", description="MD5 sum of up to the first 100MB of this file.")
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
    media_id: Optional[int] = Field(alias="media_id", description="Media ID.")
    gid: Optional[str] = Field(alias="gid", description="Upload group ID.")
    uid: Optional[str] = Field(alias="uid", description="Upload unique ID.")
    group_to: Optional[int] = Field(
        alias="group_to",
        default=1080,
        description="Vertical resolutions below this will be transcoded with "
        "multi-headed ffmpeg.",
    )
    id: Optional[Union[str, int]] = Field(
        alias="id",
        default=None,
        description="ID of job assigned by service (ignored on job creation).",
    )
    status: Optional[str] = Field(
        alias="status",
        default=None,
        description="Overall status of the job. Set by the service (ignored on job creation).",
    )
    start_time: Optional[str] = Field(
        alias="start_time",
        default=None,
        description="ISO8601 datetime string indicating start time of job."
    )
    stop_time: Optional[str] = Field(
        alias="stop_time",
        default=None,
        description="ISO8601 datetime string indicating stop time of job."
    )

    @validator("status")
    def status_enum(cls, value):
        assert value.lower() in [
            "pending",
            "running",
            "canceled",
            "succeeded",
            "failed",
        ]
        return value.lower()

    @validator("start_time", "stop_time")
    def time_iso8601(cls, value):
        return parse(value).isoformat()


Job.update_forward_refs()
