FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

ENV HADOOP_CONF_DIR=/hadoop/etc/hadoop

# Install envsubst (from gettext)
RUN apt-get update && apt-get install -y gettext

# Copy templates and scripts
COPY hadoop/templates/ /opt/templates/
COPY deploy/entrypoint.sh /opt/
COPY deploy/generate-configs.sh /opt/

# Make scripts executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh

# Run the entrypoint when the container starts
ENTRYPOINT ["/opt/entrypoint.sh"]
