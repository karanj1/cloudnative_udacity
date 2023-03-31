FROM python:3.8

COPY /techtrends /app

WORKDIR /app

#Install packages defined in the requirements.txt file
RUN pip install -r requirements.txt

#initialized with the pre-defined posts in the init_db.py file
RUN python init_db.py

EXPOSE 3111

CMD ["python", "app.py"]
