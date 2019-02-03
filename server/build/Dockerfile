FROM ubuntu:18.04

WORKDIR /opt/src
COPY ./server .

RUN apt-get update && apt-get install -y netcat postgresql-client

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
   python3 \
   python3-pip

RUN pip3 install -r /opt/src/build/requirements.txt

CMD ["python3", "/opt/src/manage.py", "runserver", "0.0.0.0:8000"]
