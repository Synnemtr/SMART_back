FROM python:3.9.13 AS dev-build
ENV TZ="Europe/Paris"
ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update \
    # postgresql-client for backups
    && apt-get install -y lsb-release \
    && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get -qq update && apt-get install postgresql-client-15 -y \
    && apt-get install gettext -y \
    && apt-get clean all
RUN echo 'export PS1="\[\033[33m\][\$SHOWN_NAME]\[\033[00m\] \w# "' >> /root/.bashrc && mkdir /code
WORKDIR /code
#COPY create_logs.sh /code/
#RUN chmod +x create_logs.sh
#CMD ["./create_logs.sh"]

COPY requirements.txt /code/
RUN pip install -r requirements.txt

FROM dev-build AS release-build
COPY . /code/
