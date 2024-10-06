FROM postgres:latest

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all git build-essential \
    && git clone --branch master https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make install \
    && rm -rf pgvector \
    && apt-get remove -y git build-essential \
    && apt-get autoremove -y

RUN echo "shared_preload_libraries = 'pgvector'" >> /usr/share/postgresql/postgresql.conf.sample
