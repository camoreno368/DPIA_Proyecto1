
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nano
WORKDIR /app
COPY basedatos /app/basedatos
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY src ./src/
VOLUME ./app/src
CMD [ "python","src/main.py" ]