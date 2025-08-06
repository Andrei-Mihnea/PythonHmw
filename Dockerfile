FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat-openbsd \
        curl \
        bash \
        ca-certificates \
        apt-utils \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Make your scripts executable
RUN chmod +x wait-for-it.sh start.sh

# Expose Flask/Gunicorn port
EXPOSE 5000

# Start using dynamic DATABASE_URL parsing inside start.sh
CMD ["./start.sh"]
