FROM python:3.11-slim

# System Dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies zuerst (besseres caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Code danach
COPY . /app

# Cloud Run Port
ENV PORT=8080

# Production Start (stabiler als plain uvicorn)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
