# Oracle XE 21c Docker Image
# Accept Oracle license at build time
FROM container-registry.oracle.com/database/express:21.3.0

USER root

RUN mkdir -p /opt/oracle/scripts/setup /opt/oracle/scripts/init \
    && chown -R oracle:oracle /opt/oracle/scripts

USER oracle

COPY --chown=oracle:oracle init.sql /opt/oracle/scripts/setup/init.sql

RUN sed -i 's|scripts setup|scripts setup|g' /opt/oracle/scripts/setup/sqlnet.ora || true

# Keep container alive after database setup
CMD oracle-xe-21c && tail -f /dev/null
