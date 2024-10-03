FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  build-essential \
  libffi-dev \
  mime-support \
  && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1 \
  PATH="/root/.local/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

WORKDIR /app


# To run off of a local wheel for testing
# RUN pip install /app/coordextract-local/*.whl

COPY . /app

RUN  poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi    


CMD ["uvicorn", "cml_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

