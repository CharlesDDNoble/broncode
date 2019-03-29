FROM debian:latest

RUN apt-get update
RUN apt-get install -y gcc python3 netcat

COPY . /broncode
WORKDIR /broncode

CMD ["python3", "receive.py"]
