FROM python:3.9

COPY Functions/requirements.txt requirements.txt

RUN set -eux; \
    apt-get update && \
    apt-get install -y build-essential && \
    python3 -m venv .venv --without-pip

RUN apt-get install -y pip

RUN pip3 install --target=".python_packages/lib/site-packages" -r requirements.txt