FROM python:3.8.6-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt upgrade -y && \
    python -m venv venv && \
    python -m pip install --upgrade pip --user && \
    pip install -r requirements.txt && \

COPY . .

CMD ["gunicorn", "backend.wsgi", "-t", "600", "-b", "0.0.0.0:8000"]