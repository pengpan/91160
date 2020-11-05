FROM python:3-alpine
LABEL maintainer="MasterPan <i@hvv.me>"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
ENV TIME_ZONE Asia/Shanghai
RUN apk add tzdata \
    && cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && apk del tzdata

RUN apk --no-cache add g++

WORKDIR /usr/src/app

COPY ["requirements.txt", "main.py", "./"]

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
