FROM arm64v8/openjdk:8-jdk-slim
# Point JAVA_HOME at ARM64’s OpenJDK install
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set up Hadoop
ENV HADOOP_VERSION=3.2.1
ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
ENV PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

# Install prerequisites for Hadoop download & unpack
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    tar \
  && rm -rf /var/lib/apt/lists/*

# Download & extract Hadoop
RUN curl -fsSL \
      https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    | tar -xz -C /opt/ \
  && rm -rf ${HADOOP_HOME}/share/doc/hadoop

# Install gettext (for envsubst) and build tools for Python/OpenSSL
ENV OPENSSL_VERSION=1.1.1w \
    PYTHON_VERSION=3.11.1
RUN apt-get update && apt-get install -y --no-install-recommends \
      gettext \
      build-essential \
      libssl-dev \
      zlib1g-dev \
      libncurses5-dev \
      libncursesw5-dev \
      libreadline-dev \
      libsqlite3-dev \
      libgdbm-dev \
      libdb5.3-dev \
      libbz2-dev \
      libexpat1-dev \
      liblzma-dev \
      tk-dev \
      libffi-dev \
      wget \
      git \
      cmake \
      libsasl2-dev \
      libzstd-dev \
      liblz4-dev \
      python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Build and install OpenSSL for Python linkage
ENV LD_LIBRARY_PATH=/usr/local/ssl/lib
RUN wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz \
  && tar xzf openssl-${OPENSSL_VERSION}.tar.gz \
  && cd openssl-${OPENSSL_VERSION} \
  && ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib \
  && make -j$(nproc) && make install \
  && cd .. && rm -rf openssl-${OPENSSL_VERSION}*

# Build and install Python 3.11.1
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
  && tar xzf Python-${PYTHON_VERSION}.tgz \
  && cd Python-${PYTHON_VERSION} \
  && ./configure --enable-optimizations --with-ensurepip=install --with-openssl=/usr/local/ssl \
  && make -j$(nproc) && make altinstall \
  && cd .. && rm -rf Python-${PYTHON_VERSION}*

# Make python3.11 & pip3.11 the defaults
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 \
 && update-alternatives --install /usr/bin/pip    pip    /usr/local/bin/pip3.11    1 \
 && python -c "import ssl; print(ssl.OPENSSL_VERSION)" \
 && pip install --upgrade pip

# Build and install librdkafka (ARM64) from source
RUN git clone https://github.com/confluentinc/librdkafka.git \
  && cd librdkafka \
  && git checkout v2.10.0 \
  && ./configure \
  && make -j$(nproc) -C src && make -j$(nproc) -C src-cpp \
  && make -j$(nproc) install -C src && make -j$(nproc) install -C src-cpp \
  && ldconfig \
  && cd .. && rm -rf librdkafka

# Install the Python bindings for confluent-kafka
RUN pip install --no-binary :all: confluent-kafka

# Copy over your templates, scripts, and MapReduce code
COPY hadoop/templates/ /opt/templates/
COPY src/mapreduce/       /src/mapreduce/
COPY deploy/entrypoint.sh /opt/
COPY deploy/generate-configs.sh /opt/

# Ensure all scripts are executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh \
    && chmod +x /src/mapreduce/mapper.py /src/mapreduce/reducer.py

# Launch via your entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]
