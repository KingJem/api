ARG TARGETPLATFORM
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.10-slim-linuxarm64
ENV HTTPS_PROXY='http://192.168.5.208:7890'

RUN apt-get update && \
    apt-get install unixodbc unixodbc-dev -y && \
    apt-get install freetds-dev freetds-bin -y 

WORKDIR /appq

COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]