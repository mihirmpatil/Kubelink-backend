FROM python:2.7.13-alpine3.6

WORKDIR /usr/src/app

EXPOSE 80

RUN apk update && apk add bash
RUN pip install flask flask-cors pyyaml
RUN apk add curl
RUN apk add git 
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.7.1/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN git clone https://github.com/jplana/python-etcd.git && cd python-etcd && python setup.py install && cd ..
RUN echo "export PATH=$PATH:/usr/src/app" >> ~/.bashrc

COPY . .
#COPY requirements.txt ./
#RUN start.sh

CMD [ "./start.sh" ]
