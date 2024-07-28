FROM python:3.12.4-alpine AS build

COPY . /src

WORKDIR /src

RUN apk update && \
  apk add gcc musl-dev linux-headers && \
  pip install poetry && \
  poetry build && \
  pip install dist/netmon_proc-*.whl

FROM python:3.12.4-alpine AS final

COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin/ /usr/local/bin

RUN apk update && \
  apk add gcc libpcap-dev

ENTRYPOINT [ "netmon-proc" ]
