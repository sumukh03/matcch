FROM python:3.10

WORKDIR /work-dir

COPY ./app/ /work-dir/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN flask db init
RUN flask db migrate 
RUN flask db upgrade

CMD ["python", "app.py"]


