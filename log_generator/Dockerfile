FROM python:3

USER root
WORKDIR /

ADD requirements.txt /
RUN pip3 install -r requirements.txt

ADD generator.py /

CMD [ "python3", "./generator.py" ]