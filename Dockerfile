FROM python:3.14.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.15 /uv /uvx /bin/

# Copy pyproject and lock file to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen --no-dev --no-install-workspace

# Copy application's code
COPY . /app/

# Streamlit's configuration options
ENV PYTHONPATH="/app"
ENV STREAMLIT_CLIENT_TOOLBAR_MODE="viewer"
ENV STREAMLIT_SERVER_PORT=8501
ENV ENVIRONMENT=production

# Expose port for the application
EXPOSE 8501

# Add healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Set the entrypoint
ENTRYPOINT ["uv", "run", "streamlit", "run", "main.py", "--server.address=0.0.0.0"]
