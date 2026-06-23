FROM python:3.12-slim

LABEL org.opencontainers.image.title="Hermes PSE Simulator"
LABEL org.opencontainers.image.description="Fake PSE bank for local Hermes payment testing"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 8099
CMD ["python", "app.py"]
