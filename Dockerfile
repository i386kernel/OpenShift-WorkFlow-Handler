FROM python:3.8-slim

LABEL Developer="Lakshya Nanjangud <lakshya.nanjangud@in.ibm.com>"

LABEL Maintainer="Openshift Team - Resiliency Orchestration"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]

