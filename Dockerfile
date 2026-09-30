FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies system-wide
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure data and persistence directories exist
RUN mkdir -p /app/outputs /app/logs /app/data

ENV PATH="/usr/local/bin:/usr/bin:/bin:/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose Streamlit dashboard (8501) and API (8000)
EXPOSE 8501 8000

# Health check against Streamlit UI
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Launch the ArchitectAI Web Platform
CMD ["python3", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

