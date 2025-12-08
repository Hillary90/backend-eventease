FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements files and install. If a minimal production requirements file
# `requirements.prod.txt` exists, prefer it to avoid complex dependency resolution
# during builds on CI/hosts like Render.
COPY requirements*.txt ./
RUN python -m pip install --upgrade pip
RUN if [ -f requirements.prod.txt ]; then \
            echo "Installing from requirements.prod.txt"; \
            pip install --no-cache-dir -r requirements.prod.txt; \
        else \
            echo "Installing from requirements.txt"; \
            pip install --no-cache-dir -r requirements.txt; \
        fi

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
