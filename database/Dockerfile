# Usando a imagem alpine do Postgres 16
FROM postgres:16-alpine

RUN apk update \
    && apk add --no-cache \
        postgresql-dev \
        git \
        build-base \
    && git clone --branch master https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make install \
    && cd .. \
    && rm -rf pgvector \
    && apk del git build-base \
    && rm -rf /var/cache/apk/*

RUN echo "shared_preload_libraries = 'pgvector'" >> /usr/local/share/postgresql/postgresql.conf.sample

RUN rm -rf /var/lib/postgresql/data/*

CMD ["postgres"]
