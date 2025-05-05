# Use official Python base image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering and set Streamlit to not prompt for updates
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pre-install dependencies to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit entrypoint
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
