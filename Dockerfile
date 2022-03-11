# syntax=docker/dockerfile:1

FROM alpine:3.14

RUN apk add --no-cache gnupg
RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip
RUN apk add --no-cache bash

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


#CMD ["bash"]
CMD [ "python3", "simplegpg.py", "--homedir", "./"]
