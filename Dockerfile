FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /lurl
WORKDIR /lurl
ADD requirements.txt /lurl/
RUN pip install -r requirements.txt
ADD . /lurl/

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
