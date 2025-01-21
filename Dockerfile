FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and cleanup
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# Create docker group (if it doesn't exist) and add our user to it
RUN groupadd -g 998 docker || true && \
    usermod -aG docker root

# Install pip and hatch
RUN pip install --no-cache-dir pip hatch

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Install the package with hatch
RUN hatch build && pip install dist/*.whl

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Create directory for project outputs
RUN mkdir -p /app/projects && \
    chmod 777 /app/projects

# Expose the port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "dev_crew.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 