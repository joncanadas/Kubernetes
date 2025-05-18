FROM python:3.11-slim
WORKDIR /app
COPY consumer1.py .
RUN pip install pika pymongo
CMD ["python", "consumer1.py"]
