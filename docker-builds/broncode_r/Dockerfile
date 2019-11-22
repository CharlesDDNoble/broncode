FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/"
RUN apt-get update
RUN apt-get -yq install --fix-missing python3 
RUN apt-get -yq install --fix-missing r-base-dev
RUN apt-get -yq install --fix-missing r-base-core
RUN apt-get -yq install --fix-missing r-base
COPY env/ .
EXPOSE 4002
CMD [ "python3", "start_r.py" ]

