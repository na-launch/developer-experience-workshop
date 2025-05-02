# Dockerfile
FROM registry.access.redhat.com/ubi8/ubi-minimal

ENV ENDPOINT localhost:5000

# Install bash and curl
USER root
RUN microdnf install bash curl && \
    microdnf clean all

# Copy the script into the container at /opt
COPY api-check.sh /opt/api-check.sh
RUN chmod +x /opt/api-check.sh

# Set the default command to run the script
ENTRYPOINT /opt/api-check.sh $ENDPOINT