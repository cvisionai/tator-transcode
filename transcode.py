from uuid import uuid1
import json
import subprocess


def transcode(job):
    """
    Does a transcode.
    """
    cmd = [
        "python3",
        "-m",
        "tator.transcode",
        "--url",
        job.url,
        "--host",
        job.host,
        "--token",
        job.token,
        "--project",
        str(job.project),
        "--type",
        str(job.type),
        "--name",
        job.name,
        "--section",
        job.section,
        "--uid",
        job.uid,
        "--gid",
        job.gid,
    ]
    if job.attributes is not None:
        cmd += ["--attributes", json.dumps(job.attributes)]
    if job.media_id is not None:
        cmd += ["--media_id", job.media_id]
    subprocess.run(cmd, check=True)
