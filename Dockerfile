FROM python:3-alpine
MAINTAINER MasterPan <i@hvv.me>
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
ENV TIME_ZONE Asia/Shanghai
RUN apk add tzdata \
    && cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && apk del tzdata
RUN apk add g++
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple
COPY main.py .
CMD [ "python", "main.py" ]
