FROM python:3.8
LABEL maintainer="noemail@website.domain"
COPY . /todo
WORKDIR /todo
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

