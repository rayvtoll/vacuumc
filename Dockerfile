FROM python:3.7-alpine
RUN apk add -U docker jq
WORKDIR /app
COPY . /app
EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["app.py"]
