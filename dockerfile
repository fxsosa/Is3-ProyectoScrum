FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY . /usr/src/app

# Actualizando el sistema e instalando lo basico, python, git, make
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git make build-essential libpq-dev python3-dev

# Lo basico para levantar
## Nodejs
RUN curl -sL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh && bash /tmp/nodesource_setup.sh 
RUN apt-get install --yes nodejs

## Postgres 
ENV TZ=America/Asuncion \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get install --yes postgresql postgresql-contrib

### configuracion del postgres
USER postgres
RUN /etc/init.d/postgresql start &&\
    createdb mydb &&\
    psql -c "ALTER USER postgres PASSWORD 'admin';" &&\
    psql mydb --command "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;"
USER root

## Pip y venv
RUN apt-get install -y python3-pip python3-venv

# instalacion de lo necesario para deployar
RUN pip install -r requirements.txt
