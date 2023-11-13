#!/bin/bash

sed 's/$SQL_PASSWORD/'"$SQL_PASSWORD"'/' -i .env.prod.db
sed 's/$SQL_PASSWORD/'"$SQL_PASSWORD"'/' -i server/.env.prod
sed 's/$MAIL_PASSWORD/'"$MAIL_PASSWORD"'/' -i server/.env.prod
sed 's/${ENV}/'"$ENV"'/' -i docker-compose.yml

# Rename docker-compose.prod.yml
mv docker-compose.prod.yml docker-compose.override.yml