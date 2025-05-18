FROM python:3.11-slim
WORKDIR /app
COPY consumer3.py .
RUN pip install pika
CMD ["python", "consumer3.py"]
