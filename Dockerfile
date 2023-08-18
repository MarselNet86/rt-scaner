FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3.8-venv

CMD ["python3", "main.py"]