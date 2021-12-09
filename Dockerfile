FROM python:3.8.12-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY check-garage.py .

CMD python -u check-garage.py
