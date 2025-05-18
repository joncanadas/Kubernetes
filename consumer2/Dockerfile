FROM python:3.11-slim
WORKDIR /app
COPY consumer2.py .
RUN pip install pika
CMD ["python", "consumer2.py"]
