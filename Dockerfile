FROM python:3.9

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]