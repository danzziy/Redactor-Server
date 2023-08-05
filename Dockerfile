FROM python:3.11.0

WORKDIR /app/

COPY . .

RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get install ffmpeg -y

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
