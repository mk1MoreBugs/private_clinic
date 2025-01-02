FROM debian:12-slim
WORKDIR ./client
COPY . .
RUN apt-get -y update && apt-get -y install default-jre
EXPOSE 8000
CMD ["./gradlew", "jsRun", "-t"]

