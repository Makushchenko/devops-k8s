FROM golang AS builder
WORKDIR /src
COPY src .
# CGO_ENABLED=0 doesn’t rely on external libraries or OS features
RUN CGO_ENABLED=0 go build -o app

FROM scratch
ADD ./html /html
COPY --from=builder /src/app .
ENTRYPOINT [ "/app" ]
EXPOSE 8080