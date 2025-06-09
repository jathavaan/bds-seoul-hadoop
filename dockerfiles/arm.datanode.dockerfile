FROM arm64v8/openjdk:8-jdk-slim

# Point JAVA_HOME at ARM64’s OpenJDK install
ARG JAVA_HOME_PATH
ENV JAVA_HOME=${JAVA_HOME_PATH}
ENV PATH=$JAVA_HOME/bin:$PATH

# Set up Hadoop
ENV HADOOP_VERSION=3.2.1
ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
ENV PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

# Install prerequisites for Hadoop download & unpack
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gettext-base \
    ca-certificates \
    tar \
  && rm -rf /var/lib/apt/lists/*
# Download & extract Hadoop
RUN curl -fsSL \
      https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    | tar -xz -C /opt/ \
  && rm -rf ${HADOOP_HOME}/share/doc/hadoop

# Copy over your templates and entrypoint scripts
COPY hadoop/templates/       /opt/templates/
COPY deploy/entrypoint.sh   /opt/
COPY deploy/generate-configs.sh /opt/

# Ensure all scripts are executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh

# Launch via your entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]
