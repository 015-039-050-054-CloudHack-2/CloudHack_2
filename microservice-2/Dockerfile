FROM python:3

WORKDIR /usr/src/app
RUN apt-get update
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install pymongo

# EXPOSE 27017
COPY . .

CMD [ "python", "-u", "a2.py" ]

