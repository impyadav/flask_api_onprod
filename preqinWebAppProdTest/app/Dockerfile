FROM python:3.9.15

WORKDIR /flask_app

COPY . /flask_app

RUN pip install -r /flask_app/requirements.txt

# CMD ["gunicorn"  , "--bind", "0.0.0.0:8989", "server:flaskApplication"]

# CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "--log-file", "onlinePredApp.log", \
#  "--log-level", "onlinePredApp.log", "--access-logfile", "onlinePredApp.log", "--error-logfile", \
#   "onlinePredApp.log", "server:flaskApplication"]