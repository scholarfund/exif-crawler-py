FROM --platform=linux/amd64 python:3.12-bookworm

WORKDIR /usr/src/app

RUN python3 -m pip install --no-cache-dir requests pillow beautifulsoup4

COPY main.py .

CMD ["python3", "./main.py"]
