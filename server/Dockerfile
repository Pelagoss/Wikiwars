###########
# BUILDER #
###########
FROM python:3.9-slim-bookworm as builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies only
# Nettoyage immédiat pour ne pas alourdir les layers intermédiaires (bonne pratique)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Optimisation CACHE: On copie uniquement requirements d'abord
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

#########
# FINAL #
#########
FROM python:3.9-slim-bookworm as backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/app \
    APP_HOME=/home/app/server

# Create user and directory structure
RUN addgroup --system app && \
    adduser --system --group app && \
    mkdir -p $APP_HOME

WORKDIR $APP_HOME

# Install system runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies from builder
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy project files AND set permissions simultaneously
# Remplace le coûteux "RUN chown -R"
COPY --chown=app:app . $APP_HOME

# Ensure execution rights
RUN chmod +x entrypoint.sh

USER app

ENTRYPOINT ["./entrypoint.sh"]