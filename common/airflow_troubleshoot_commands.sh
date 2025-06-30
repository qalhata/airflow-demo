#!/bin/bash

echo "1. Check if airflow-webserver container is running:"
docker-compose ps airflow-webserver

echo "2. If not running, start the webserver container and watch logs:"
echo "docker-compose up airflow-webserver"

echo "3. If running, check logs for errors:"
echo "docker-compose logs airflow-webserver"

echo "4. Verify the webserver is binding to 0.0.0.0 and port 8080 inside the container:"
echo "docker exec -it \$(docker-compose ps -q airflow-webserver) netstat -tuln | grep 8080"

echo "5. Check if port 8080 is accessible from host:"
echo "curl http://localhost:8080"

echo "6. If UI is not accessible, check firewall or Docker network settings on port 8080."

echo "7. Use default credentials admin/admin to login if authentication is enabled."
