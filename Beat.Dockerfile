# Use the specified Python version
#ARG PYTHON_VERSION=3.11-slim-bookworm
ARG PYTHON_VERSION=3.10-slim-bookworm
FROM python:${PYTHON_VERSION}

# Install necessary dependencies, including libgl1 for OpenCV
RUN apt-get update && apt-get install --no-install-recommends -y \
  git \
  build-essential \
  libpq-dev \
  libgl1 \
  libglib2.0-0 libsm6 libxrender1 libxext6 \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY . .

CMD ["celery", "-A", "infrastructure.celery_setup.celery_config", "beat", "--loglevel=info"]