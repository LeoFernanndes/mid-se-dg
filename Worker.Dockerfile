ARG PYTHON_VERSION=3.10-slim-bookworm
FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install --no-install-recommends -y \
  git \
  build-essential \
  libpq-dev \
  libgl1 \
  libglib2.0-0 libsm6 libxrender1 libxext6 \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "-A", "infrastructure.celery_setup.celery_config", "worker", "--loglevel=info"]