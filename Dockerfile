FROM python:latest
COPY app.py /
COPY requirements.txt /
COPY apirequest.py /
RUN pip install -r requirements.txt
EXPOSE 8050
CMD [ "python", "./app.py" ]
