# Stage 1: Builder - installs dependencies
FROM python:3.9-slim-buster AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final image - optimized for production
FROM python:3.9-slim-buster
WORKDIR /app
COPY chat_history_service.py .
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
COPY --from=builder /install /usr/local
USER appuser
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 5002
# Change the CMD to use waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5002", "chat_history_service:app"]
