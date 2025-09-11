# PostgreSQL Dockerfile for production database
FROM postgres:15-alpine

# Set environment variables
ENV POSTGRES_DB=cost_optimization
ENV POSTGRES_USER=cost_user
ENV POSTGRES_PASSWORD=cost_password

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Expose port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1
