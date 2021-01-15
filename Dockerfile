FROM python:3
WORKDIR /code
COPY . .
RUN apt-get install gcc
RUN pip install -r requirements.txt
RUN pip install -e .