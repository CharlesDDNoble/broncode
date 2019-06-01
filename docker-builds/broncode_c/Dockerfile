FROM ubuntu:18.04
# We need python3 to run start.py
RUN apt-get update && apt-get -y install python3 gcc
COPY start_c.py .
COPY executors /executors
EXPOSE 4000
CMD [ "python3", "start_c.py" ]

