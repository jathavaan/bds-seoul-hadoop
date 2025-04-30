FROM ubuntu:latest
LABEL authors="jatha"

ENTRYPOINT ["top", "-b"]