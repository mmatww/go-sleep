FROM golang:1.19-alpine3.16 as builder

RUN apk add git

ADD . /app
WORKDIR /app
RUN go mod download && go build -o server ./server && go build -o client ./client

FROM alpine:3.16
RUN apk add ca-certificates
COPY --from=builder /app/server /app/client /

CMD ["./server"]
