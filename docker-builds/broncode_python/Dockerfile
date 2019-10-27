FROM ubuntu:18.04
RUN apt-get update && apt-get -y install python3
COPY env/ .
EXPOSE 4001
CMD [ "python3", "start_python.py" ]

