FROM python:3.7-alpine
COPY app.py app/
COPY requirements.txt app/
COPY apirequest.py app/
COPY assets app/assets/
RUN pip install -r app/requirements.txt
EXPOSE 8050
CMD python app/app.py