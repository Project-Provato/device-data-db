FROM grafana/grafana-oss:11.4.0

# copy config files
COPY ./config/datasources.yaml /etc/grafana/provisioning/datasources/main.yaml
COPY ./config/dashboards.yaml /etc/grafana/provisioning/dashboards/main.yaml
# all preconfigured dashboards
COPY ./config/dashboards/ /var/lib/grafana/dashboards/
# grafana ini settings
COPY ./config/grafana.ini /etc/grafana/grafana.ini
# pass grafana new icons for geomap
# COPY ./icons/ /usr/share/grafana/public/img/icons/animals/

# Arguments
ARG GRAFANA_USER
ARG GRAFANA_PASS

# Default grafana url
ARG GRAFANA_URL

# Timescale Arguments
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASS
ARG POSTGRES_DB

ENV GF_SERVER_ROOT_URL=${GRAFANA_URL}
ENV GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASS}

# Change datasource based on env
# RUN sed -i "s#data-url#${API_URL}/api/db#g" /etc/grafana/provisioning/datasources/main.yaml

RUN sed -i "s#POSTGRES_HOST#${POSTGRES_HOST}#" /etc/grafana/provisioning/datasources/main.yaml
RUN sed -i "s#POSTGRES_PORT#${POSTGRES_PORT}#" /etc/grafana/provisioning/datasources/main.yaml
RUN sed -i "s#POSTGRES_USER#${POSTGRES_USER}#" /etc/grafana/provisioning/datasources/main.yaml
RUN sed -i "s#POSTGRES_PASS#${POSTGRES_PASS}#" /etc/grafana/provisioning/datasources/main.yaml
RUN sed -i "s#POSTGRES_DB#${POSTGRES_DB}#" /etc/grafana/provisioning/datasources/main.yaml

EXPOSE 3000