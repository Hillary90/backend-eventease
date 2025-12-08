FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Copy entrypoint/start script and make executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

# Use the start script so we can write serviceAccountKey.json from env at container start
ENTRYPOINT ["/app/start.sh"]
