FROM python:slim-bullseye

WORKDIR /srechallenge

COPY requirements.txt requirements.txt
COPY app.py app.py
RUN pip3 install -r requirements.txt

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]