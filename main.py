import os
from typing import Dict, List, Union
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
from redis import Redis
from rq import Queue
from rq.job import Job as Qjob
from models.job import Job
from models.response import Response
from transcode import transcode

app = FastAPI(
    title="Transcode",
    description="Simple transcode API",
    version="0.0.0",
)


def _qjob_to_job(qjob):
    job = qjob.args[0]
    status = qjob.get_status(refresh=True)
    if status in ["queued", "deferred", "scheduled"]:
        job.status = "pending"
    if status == "started":
        job.status = "running"
    if status in ["canceled", "stopped"]:
        job.status = "canceled"
    if status == "finished":
        job.status = "completed"
    if status == "failed":
        job.status = status
    job.id = qjob.id
    return job


def get_queue():
    rds = Redis(host=os.getenv("REDIS_HOST"))
    queue = Queue("transcodes", connection=rds)
    return rds, queue


def append_value(rds, key, value):
    value_list = rds.get(key)
    if value_list is None:
        rds.set(key, value)
    else:
        rds.set(key, value_list + f",{value}")


def get_list(rds, key):
    value_list = rds.get(key)
    if value_list is None:
        value_list = []
    else:
        value_list = value_list.split(",")
    return value_list


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
def jobs_delete(
    uid_list: List[str] = Body(default=None),
    gid: Union[str, None] = None,
    project: Union[int, None] = None,
) -> Response:
    rds, queue = get_queue()
    if gid is not None:
        uid_list = get_list(gid)
    elif project is not None:
        uid_list = get_list(project)
    elif uid_list is None:
        raise Exception("At least one parameter specifying jobs must be provided!")
    job_list = Qjob.fetch_many(uid_list, connection=rds)
    for job in job_list:
        job.cancel()
    return Response(message="Successfully canceled {len(job_list)} jobs!")


@app.post(
    "/jobs",
    responses={
        201: {"model": List[Job], "description": "List of created jobs."},
        400: {"description": "Error creating the transcode jobs."},
    },
    tags=["Transcode"],
    summary="Create one or more transcode jobs.",
    response_model_by_alias=True,
)
def jobs_post(job_list: List[Job]) -> Response:
    rds, queue = get_queue()
    qjob_list = []
    for job in job_list:
        if job.uid is None:
            job.uid = str(uuid1())
        if job.gid is None:
            job.gid = str(uuid1())
        append_value(job.gid, job.uid)
        append_value(f"project_{job.project}", job.uid)
        qjob_list.append(queue.enqueue(transcode, job, job_id=job.uid))
    return [_qjob_to_job(job) for job in qjob_list]


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
def jobs_put(
    uid_list: List[str] = Body(default=None),
    gid: Union[str, None] = None,
    project: Union[int, None] = None,
) -> List[Job]:
    rds, queue = get_queue()
    if gid is not None:
        uid_list = get_list(gid)
    elif project is not None:
        uid_list = get_list(project)
    elif uid_list is None:
        raise Exception("At least one parameter specifying jobs must be provided!")
    job_list = Qjob.fetch_many(uid_list, connection=rds)
    return [_qjob_to_job(job) for job in qjob_list]
