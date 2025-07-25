FROM python:3.11-slim

WORKDIR /app

# Install netcat for wait-for-it.sh
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x wait-for-it.sh

CMD ["python", "main.py"]
