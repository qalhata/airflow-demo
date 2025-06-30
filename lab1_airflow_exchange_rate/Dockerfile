# Use a specific, stable version of Airflow. This is crucial for reproducibility.
FROM apache/airflow:2.9.2

# Switch to the root user ONLY to install system packages.
USER root

# Install git, which is needed by one of your providers or for other tasks.
# The '&& \' syntax chains commands efficiently and keeps layers small.
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# IMPORTANT: Switch back to the non-root 'airflow' user for all subsequent operations.
# This is a critical security best practice.
USER airflow

# Copy your requirements file into the container's Airflow home directory.
# The --chown flag ensures the 'airflow' user owns the file.
COPY --chown=airflow:airflow airflow/requirements.txt /opt/airflow/requirements.txt

# Upgrade pip and then install your Python dependencies.
# Upgrading pip can resolve complex dependency resolution issues that might
# corrupt the environment.
# Using a constraints file is the recommended way to install providers and
# dependencies to avoid conflicts.
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.12.txt"