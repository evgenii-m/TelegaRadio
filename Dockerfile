#Python based docker image
FROM python:3.11.9

RUN apt-get update && apt-get upgrade -y

#Installing Requirements
RUN apt-get install --fix-missing -y curl ffmpeg libavformat-dev libavdevice-dev python3-pip opus-tools

#Updating pip
RUN python3 -m pip install -U pip

MKDIR radio_data

COPY . .

RUN python3 -m pip install -U -r requirements.txt

CMD ["python3", "main.py"]
