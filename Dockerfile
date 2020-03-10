FROM python:latest
COPY app.py app/
COPY requirements.txt app/
COPY apirequest.py app/
COPY assets app/assets/
RUN pip3 install -r app/requirements.txt
EXPOSE 8050
CMD python app/app.py