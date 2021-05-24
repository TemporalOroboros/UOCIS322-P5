FROM python:3.8
LABEL maintainer=ekillen@uoregon.edu
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /webapp
WORKDIR /webapp
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
