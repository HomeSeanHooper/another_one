FROM python:3.7


ENV PYTHONPATH=/usr/src/app

WORKDIR /usr/src/app
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .
EXPOSE 8080
CMD ["python", "-u", "twistd_app.py"]
