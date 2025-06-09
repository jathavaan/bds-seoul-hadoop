FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# Point JAVA_HOME correctly so Hadoop’s scripts find java
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

ENV HADOOP_HOME=/opt/hadoop-3.2.1
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install envsubst (gettext) so that generate-configs.sh can template XML files
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

# Copy Hadoop templates and entrypoint scripts
COPY hadoop/templates/ /opt/templates/
COPY deploy/entrypoint.sh /opt/
COPY deploy/generate-configs.sh /opt/

# Make entrypoint and templating scripts executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh

ENTRYPOINT ["/opt/entrypoint.sh"]
