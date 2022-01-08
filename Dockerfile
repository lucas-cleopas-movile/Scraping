FROM selenium/standalone-chrome

WORKDIR /app
COPY . ./

RUN sudo apt-get update -y
RUN sudo apt-get install python3 python3-pip -y

RUN pip3 install -r requirements.txt

CMD python3 main.py