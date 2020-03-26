FROM python:3

WORKDIR /usr/src/app
USER root
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./ ./

EXPOSE 8080

CMD ["python3", "main.py"]