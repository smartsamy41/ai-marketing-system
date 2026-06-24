FROM python:3.11-slim

WORKDIR /app

# =========================
# INSTALL DEPENDENCIES
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# COPY CODE
# =========================
COPY app ./app
COPY engine ./engine

# =========================
# ENVIRONMENT
# =========================
ENV PYTHONPATH=/app
ENV PORT=8080

# =========================
# START COMMAND (CRITICAL FIX)
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
