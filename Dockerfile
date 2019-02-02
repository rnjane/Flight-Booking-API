FROM ubuntu:16.04
LABEL maintainer="Robert Njane <robert.njane@andela.com>"

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-setuptools
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev \
libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:chris-lea/redis-server
RUN apt-get install -y redis-server
RUN apt-get install -y python-virtualenv
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN apt-get clean

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD src/requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/

COPY celeryd /etc/default/celeryd
COPY init.d/celeryd /etc/init.d/celeryd
COPY init.d/celerybeat /etc/init.d/celerybeat
COPY startscript.sh /usr/bin/start
RUN chmod +x /usr/bin/start

RUN chmod 755 /etc/init.d/celeryd
RUN chmod 755 /etc/init.d/celerybeat

RUN python3 src/manage.py migrate --noinput

EXPOSE 8000
ENTRYPOINT ["/usr/bin/start"]