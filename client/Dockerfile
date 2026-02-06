#syntax=docker/dockerfile:1

# 1. Étape de build
# On fixe la version (ex: Node 20) pour éviter les surprises lors des mises à jour automatiques de "lts"
FROM node:20-alpine AS build-stage

WORKDIR /app

# Copie des fichiers de dépendances
COPY package*.json ./

# 'npm ci' est beaucoup plus rapide et fiable que 'npm install' pour les builds de prod
# Il exige la présence d'un package-lock.json
RUN npm ci

# Copie du code source et build
COPY . .
RUN npm run build

# 2. Étape de production
FROM nginx:1.26-alpine AS production-stage

# Nettoyage du dossier par défaut de Nginx avant la copie
RUN rm -rf /usr/share/nginx/html/*

# Copie des artefacts compilés
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
