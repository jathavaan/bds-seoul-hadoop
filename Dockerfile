FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

ENV HADOOP_HOME=/opt/hadoop-3.2.1
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

ENV PYTHON_VERSION=3.11.1
ENV OPENSSL_VERSION=1.1.1w
ENV LD_LIBRARY_PATH="/usr/local/ssl/lib"

# Install envsubst (from gettext)
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y gettext

# Install dependencies for envsubst and Python build
RUN apt-get install -y \
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
    curl \
    && rm -rf /var/lib/apt/lists/*

# Build and install Python 3.11.1 with SSL support
RUN wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz && \
    tar -xzf openssl-${OPENSSL_VERSION}.tar.gz && \
    cd openssl-${OPENSSL_VERSION} && \
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib && \
    make -j$(nproc) && \
    make install && \
    cd .. && rm -rf openssl-${OPENSSL_VERSION}*

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations --with-ensurepip=install --with-openssl=/usr/local/ssl && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && rm -rf Python-${PYTHON_VERSION}*

# Make python3.11 the default python and pip
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.11 1

# Verify Python and SSL support
RUN python -c "import ssl; print(ssl.OPENSSL_VERSION)" && \
    pip install --upgrade pip

# Copy templates and scripts
COPY hadoop/templates/ /opt/templates/
COPY deploy/entrypoint.sh /opt/
COPY deploy/generate-configs.sh /opt/

# Make scripts executable
RUN chmod +x /opt/entrypoint.sh /opt/generate-configs.sh
RUN chmod +x ./src/mapreduce/mapper.py ./src/mapreduce/reducer.py

# Run the entrypoint when the container starts
ENTRYPOINT ["/opt/entrypoint.sh"]
