FROM python:3.11-slim as requirements-stage

WORKDIR /app

COPY . /app

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m ensurepip --default-pip && \
    python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

ENV NAME=stg

CMD ["python", "run_api.py"]
