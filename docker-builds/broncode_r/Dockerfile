FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -yq install python3 r-base
COPY env/ .
EXPOSE 4002
CMD [ "python3", "start_r.py" ]

