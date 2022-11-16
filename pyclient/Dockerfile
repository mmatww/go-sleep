FROM python:3.9-slim as base

FROM base as builder
WORKDIR /app
ADD requirements.txt .
RUN python -m venv ./env && ./env/bin/pip install --upgrade pip && ./env/bin/pip install -r ./requirements.txt

FROM base
COPY --from=builder /app /app
WORKDIR /app
ADD *.py* .

ENTRYPOINT ["/app/env/bin/python"]
