FROM python:3-alpine

RUN apk add --no-cache git

LABEL org.opencontainers.image.source=https://github.com/realiserad/gitlab-jobs
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /jobs

COPY jobs .
