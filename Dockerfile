FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

EXPOSE 8006

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./app

CMD [ "python", "./app/run.py" ]