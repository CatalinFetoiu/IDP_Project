FROM python:3

USER root
WORKDIR /

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD client.py /

CMD [ "python3", "./client.py", "elasticsearch_service" ]