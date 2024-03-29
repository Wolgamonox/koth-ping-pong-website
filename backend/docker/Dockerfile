# Base off the official python image
# Define a common stage for dev and prod images called base
FROM python:3.11 as base

# Set en
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a user to avoid running as root in production
RUN addgroup --system web \
    && adduser --system --ingroup web web

# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
    # dependencies for building Python packages
    build-essential \
    # postgress client (psycopg2) dependencies
    libpq-dev \
    # cleaning up unused files to reduce the image size
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# Switch to the non-root user
USER web
# Create a directory for the source code and use it as base path
WORKDIR /home/web/code/
# Copy the python depencencies list for pip
COPY --chown=web:web ./requirements/base.txt requirements/base.txt

# Switch to the root user temporary, to grant execution permissions.
USER root
# Install python packages at system level
RUN pip install --no-cache-dir -r requirements/base.txt
# Copy entrypoint script which waits for the db to be ready
COPY --chown=web:web ./docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to the non-root user
USER web
# This script will run before every command executed in the container
ENTRYPOINT ["entrypoint.sh"]


# Define an image for local development. Inherits common packages from the base stage.
FROM base as dev
# Install extra packages required in development
USER root
COPY --chown=web:web ./requirements/dev.txt requirements/dev.txt
RUN pip install --no-cache-dir -r requirements/dev.txt
# Copy the scripts that starts the development application server (runserver)
COPY --chown=web:web ./docker/start-dev-server.sh /usr/local/bin/start-dev-server.sh
RUN chmod +x /usr/local/bin/start-dev-server.sh
USER web
# The development server starts by default when the container starts
CMD ["start-dev-server.sh"]


# Define an image for production. Inherits common packages from the base stage.
FROM base as prod
# Install extra packages required in production
USER root
COPY --chown=web:web ./requirements/prod.txt requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
# Copy the script that starts the production application server (gunicorn)
COPY --chown=web:web ./docker/start-prod-server.sh /usr/local/bin/start-prod-server.sh
RUN chmod +x /usr/local/bin/start-prod-server.sh
USER web
# Copy the source code of our django app to the working directoy
COPY --chown=web:web ../backend ./
# The production server starts by default when the container starts
CMD ["start-prod-server.sh"]