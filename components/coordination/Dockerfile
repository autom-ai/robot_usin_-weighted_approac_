FROM alpine:3.17.1

RUN apk add --no-cache python3 py3-pip \
    && pip3 install paho-mqtt \
    && apk del py3-pip

WORKDIR /app

COPY main.py .

ENTRYPOINT [ "python3" ]

CMD ["-u","main.py"]