FROM python:3.11-slim

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy source code and assets
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run API & Web Dashboard
CMD ["python", "main.py", "--stage", "serve", "--host", "0.0.0.0", "--port", "8000"]
