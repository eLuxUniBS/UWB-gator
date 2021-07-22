FROM python:3
ARG HOST
ARG PORT
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /srv/
COPY ./ ./
RUN ls -ahl
RUN pip install --no-cache-dir -r docs/install/requirements.txt
ENV DOCKER_ENV=1
ENV PORT=$PORT
ENV HOST=$HOST