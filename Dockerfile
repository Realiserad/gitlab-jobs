FROM python:3-alpine

LABEL org.opencontainers.image.source=https://github.com/realiserad/gitlab-jobs
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /jobs

COPY requirements.txt .
COPY jobs .

RUN apk add --no-cache git && \
    pip3 install -r requirements.txt
