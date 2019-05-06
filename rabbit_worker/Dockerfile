FROM python:3

USER root
WORKDIR /

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD worker.py /

CMD [ "python3", "./worker.py", "rabbitmq_service" ]