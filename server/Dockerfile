###########
# BUILDER #
###########

# pull official base image
FROM python:3.9-slim-bookworm as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY . /app/

RUN chmod +x ./entrypoint.sh

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9-slim-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/server
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install system dependencies
RUN apt-get update && apt-get install -y netcat
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

RUN chmod +x /home/app/server/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/home/app/server/entrypoint.sh"]
