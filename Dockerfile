FROM python:3.7.4-alpine

ADD requirements.txt /

ADD app/app.py /

RUN pip install -r /requirements.txt

CMD ["python", "/app.py"]