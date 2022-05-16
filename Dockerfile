FROM python:3.8-slim

LABEL Developer="Lakshya Nanjangud"

LABEL Maintainer="Openshift Team - Resiliency Orchestration"

WORKDIR /usr/src/app

#RUN groupadd --gid 1000 rouser && useradd --uid 1000 --gid rouser --shell /bin/bash --create-home rouser
#
#USER rouser
#
#COPY --chown requirements.txt .
#
#RUN pip install --no-cache-dir requirements.txt
#
#COPY --chown . .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
