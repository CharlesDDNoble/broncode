FROM ubuntu:18.04
# We need python3 to run start.py
RUN apt-get update && apt-get -y install python3 gcc
COPY start.py .
COPY executors /executors
CMD [ "python3", "start.py" ]

