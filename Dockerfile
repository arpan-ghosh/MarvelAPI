FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
                                sqlite sqlite3

COPY . .

CMD [ "python3", "./IntelGatherer.py"]