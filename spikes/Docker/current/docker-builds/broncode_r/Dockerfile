FROM r-base:latest
# We need python3 to run start.py
RUN apt-get update && apt-get -y install python3
COPY start.py .
COPY executors /executors
CMD [ "python3", "start.py" ]

