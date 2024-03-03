FROM python:3.10
RUN groupadd djangogroup && useradd -m -g djangogroup -s /bin/bash django
WORKDIR /app
ADD src /app
COPY ./local_run.sh /
RUN apt-get update
RUN apt-get -y install cron
RUN pip3 install -r requirements.txt
COPY src/num_data/management/commands/crontab_job /etc/cron.d/crontab_job
COPY src/num_data/management/commands/docker-entrypoint.sh /
RUN crontab /etc/cron.d/crontab_job
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]