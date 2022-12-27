A lightweight transcode service
===============================

To install dependencies:

```
pip3 install -r requirements.txt
```

To run the server:
```
uvicorn main:app --reload
```

To build the docker image:
```
docker build -t transcode-service .
```

To run a container:
```
docker run -it --rm transcode-service
```

To enable auto-formatting prior to commits (developers only):
```
pre-commit install
```
