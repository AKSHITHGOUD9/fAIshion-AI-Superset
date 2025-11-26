FROM apache/superset:latest

USER root

# 1. Install the Trino driver and pin SQLAlchemy to version 1.4 (Critical for stability)
RUN pip install --no-cache-dir \
    --target=/app/pythonpath \
    "sqlalchemy-trino" \
    "sqlalchemy==1.4.49"

# 2. INJECT THE CONFIG: Copy our local config file into the container's path
COPY superset_config.py /app/pythonpath/superset_config.py

# 3. Fix permissions so the 'superset' user can read the files
RUN chown -R superset:superset /app/pythonpath

USER superset