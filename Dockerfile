FROM python:3.11-slim

RUN pip install -r requirements.txt

CMD python main.py