# docker file for python and run fast API at port 8080
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1
ENV TIME_ZONE +7
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]