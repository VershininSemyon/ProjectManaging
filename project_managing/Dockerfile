
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r -g 1000 groupdjango && \
    useradd -r -u 1000 -g groupdjango userdj

WORKDIR /app

COPY --chown=userdj:groupdjango requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=userdj:groupdjango . .

USER userdj
