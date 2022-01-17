FROM python:slim-buster

RUN apt-get update -y
RUN apt-get install -y firefox-esr

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

# Give write permission
# RUN chmod +w data/

CMD python main.py