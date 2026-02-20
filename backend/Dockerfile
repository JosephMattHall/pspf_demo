FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install pdm

# Configure PDM to not create a virtualenv
RUN pdm config python.use_venv false

# Copy dependency files
COPY pyproject.toml pdm.lock* README.md ./

# Export requirements and install dependencies globally
# We run `pdm lock` first to ensure a lockfile exists, then export.
RUN pdm lock --update-reuse && \
    pdm export -f requirements --without-hashes > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code to /app/backend
COPY . backend/

# Set PYTHONPATH to include /app so "backend" package is discoverable
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Command to be overridden by docker-compose for dev/worker
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
