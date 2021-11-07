FROM python:3.7-slim-buster

LABEL maintainer="MasterPan <327069739@qq.com>"

ENV TZ Asia/Shanghai

WORKDIR /usr/src/app

COPY ["requirements.txt", "main.py", "./"]

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
