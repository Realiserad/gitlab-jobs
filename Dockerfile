FROM python:3-alpine

LABEL org.opencontainers.image.source=https://github.com/realiserad/gitlab-jobs
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /jobs

COPY jobs .
