FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN addgroup -S appuser && \
    adduser -S appuser -G appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
