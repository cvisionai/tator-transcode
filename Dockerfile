FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY main.py .
COPY config.py .
COPY models ./models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
