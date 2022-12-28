from typing import Dict, List
from fastapi import (
    FastAPI,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)
from models.filter import Filter
from models.job import Job
from models.response import Response

app = FastAPI(
    title="Transcode",
    description="Simple transcode API",
    version="0.0.0",
)


@app.delete(
    "/jobs",
    responses={
        200: {"model": Response, "description": "Successful deletion of jobs."},
        400: {"description": "Error deleting the transcode jobs."},
    },
    tags=["Transcode"],
    summary="Deletes a list of running transcodes.",
    response_model_by_alias=True,
)
def jobs_delete(filter_list: List[Filter]) -> Response:

    ...


@app.post(
    "/jobs",
    responses={
        201: {"model": Response, "description": "Successful creation of jobs."},
        400: {"description": "Error creating the transcode jobs."},
    },
    tags=["Transcode"],
    summary="Create one or more transcode jobs.",
    response_model_by_alias=True,
)
def jobs_post(job_list: List[Job]) -> Response:
    ...


@app.put(
    "/jobs",
    responses={
        200: {"model": List[Job], "description": "List of running jobs."},
        400: {"description": "Error retrieving the transcode jobs."},
    },
    tags=["Transcode"],
    summary="Returns a list of running transcodes.",
    response_model_by_alias=True,
)
def jobs_put(filter_list: List[Filter]) -> List[Job]:
    ...
