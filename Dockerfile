FROM python:slim-buster

RUN apt-get update -y
RUN apt-get install -y firefox-esr
RUN apt-get install -y xvfb
RUN apt-get install -y x11-utils

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

# Give write permission
# RUN chmod +w data/

CMD python main.py