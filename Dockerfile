FROM python:3.8-alpine

RUN apk add --no-cache gcc libc-dev unixodbc-dev curl

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --trusted-host=pypi.python.org -r /app/requirements.txt
RUN pip install --no-cache-dir --trusted-host=pypi.python.org gunicorn

COPY ./src /app/src

ENV PYTHONPATH /app
WORKDIR "/app"

CMD ["gunicorn", "-b", "0.0.0.0:10010", "--preload", "src.main"]
#, "--logger_class", "loguru.logger.Logger"]