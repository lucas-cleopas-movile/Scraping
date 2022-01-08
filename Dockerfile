FROM selenium/standalone-chrome

WORKDIR /app
COPY . ./

RUN apt-get update
RUN apt-get install python-3.8 python-pip

RUN pip3 install -r requirements.txt

CMD python3 main.py