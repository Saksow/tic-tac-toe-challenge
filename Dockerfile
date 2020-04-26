FROM python:3.6-slim

# Install Poetry for dependency management and Gunicorn for production server
RUN pip install poetry==1.0.0 gunicorn==20.0.4

WORKDIR /app

# Copy and install dependecies first to make use Docker caching
COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

ENV APP_ENV production
ENV APP_HOST 0.0.0.0
ENV APP_PORT 5000
ENV APP_STORAGE_HOST redis
ENV APP_STORAGE_PORT 6379

COPY . .

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
