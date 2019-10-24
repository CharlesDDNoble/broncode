FROM ubuntu:18.04
RUN apt-get update && apt-get -y install python3
COPY start.py .
COPY codeserver.py .
COPY executors /executors
CMD [ "python3", "start.py" ]

