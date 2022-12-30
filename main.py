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


def get_queue():
    rds = Redis(host=os.getenv("REDIS_HOST"))
    queue = Queue("transcodes", connection=redis)
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
    uid: Union[str, None] = None,
    gid: Union[str, None] = None,
    project: Union[int, None] = None,
) -> Response:
    rds, queue = get_queue()
    job_list = []
    if uid is not None:
        job = Qjob.fetch(uid, connection=rds)
        job_list.append(job)
    elif gid is not None:
        uid_list = get_list(gid)
        job_list += Qjob.fetch_many(uid_list, connection=rds)
    elif project is not None:
        uid_list = get_list(project)
        job_list += Qjob.fetch_many(uid_list, connection=rds)
    for job in job_list:
        job.cancel()
    return Response(message="Successfully deleted {len(job_list)} jobs!")


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
    rds, queue = get_queue()
    for job in job_list:
        if job.uid is None:
            job.uid = str(uuid1())
        if job.gid is None:
            job.gid = str(uuid1())
        append_value(job.gid, job.uid)
        append_value(f"project_{job.project}", job.uid)
        queue.enqueue(transcode, job, job_id=job.uid)
    return job_list


@app.get(
    "/jobs",
    responses={
        200: {"model": List[Job], "description": "List of running jobs."},
        400: {"description": "Error retrieving the transcode jobs."},
    },
    tags=["Transcode"],
    summary="Returns a list of running transcodes.",
    response_model_by_alias=True,
)
def jobs_get(
    uid: Union[str, None] = None,
    gid: Union[str, None] = None,
    project: Union[int, None] = None,
) -> List[Job]:
    rds, queue = get_queue()
    job_list = []
    if uid is not None:
        job = Qjob.fetch(uid, connection=rds)
        job_list.append(job)
    elif gid is not None:
        uid_list = get_list(gid)
        job_list += Qjob.fetch_many(uid_list, connection=rds)
    elif project is not None:
        uid_list = get_list(project)
        job_list += Qjob.fetch_many(uid_list, connection=rds)
    job_list = [job.args[0] for job in job_list]
    return job_list
