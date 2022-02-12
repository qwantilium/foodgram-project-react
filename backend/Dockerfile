FROM python:3.8.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "backend.wsgi", "-t", "600", "-b", "0.0.0.0:8000"]