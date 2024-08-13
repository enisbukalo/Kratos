FROM python:3.11.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENTRYPOINT ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]