FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# Install envsubst (from gettext)
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y gettext

# Copy templates and scripts
COPY hadoop/templates/ /opt/templates/
COPY deploy/entrypoint.sh /opt/
COPY deploy/generate-configs.sh /opt/

# Make scripts executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh

# Run the entrypoint when the container starts
ENTRYPOINT ["/opt/entrypoint.sh"]

ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
