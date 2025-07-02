FROM python:3.9-slim

WORKDIR /app

COPY ../flask_app.py /app/flask_app.py
COPY ../fastapi_app.py /app/fastapi_app.py


RUN pip install flask

EXPOSE 5000


# if using FastAPI ( which is very popularly known to be faster) and
# indeed better for enterprise grade implementations

# ======================================== #
# We would replace COPY with FastAPI file
# We would change pip install flask to pip install fastapi uvicorn
# we would change the CMD to uvicorn nlp_fastapi_api:app --host 0.0.0.0 --port 5000


# Default: run Flask
CMD ["python", "flask_app.py"]

# To switch to FastAPI: override CMD in docker-compose.override.yml or use ENTRYPOINT override
# CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "5000"]

