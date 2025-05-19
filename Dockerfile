FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt 

EXPOSE 8000

COPY . . 

CMD [ "python3", "app/main.py" ]