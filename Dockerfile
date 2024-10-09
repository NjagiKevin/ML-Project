FROM python:3.8-buster
WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip
RUN python -m pip install awscli

RUN python -m pip install -r requirements.txt
CMD ["python3", "app.main.py"]

