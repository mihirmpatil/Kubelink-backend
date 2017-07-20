FROM python:2.7.13-alpine3.6

WORKDIR /usr/src/app

EXPOSE 5000

RUN apk update && apk add bash
RUN pip install flask flask-cors 
RUN apk add curl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.6.3/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl

COPY . .
#COPY requirements.txt ./
#RUN start.sh

CMD [ "./start.sh" ]
