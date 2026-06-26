FROM python:3.11-slim

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# WORKDIR
# =========================
WORKDIR /app

# =========================
# COPY PROJECT
# =========================
COPY . /app

# =========================
# PYTHON DEPENDENCIES
# =========================
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# ENV
# =========================
ENV PORT=8080

# =========================
# START APP
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
