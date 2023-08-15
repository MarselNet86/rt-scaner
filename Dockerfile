FROM python:3.11-slim

COPY requirements.txt /rt-scaner/requirements.txt

RUN python3 -m pip install -r /rt-scaner/requirements.txt

CMD python main.py