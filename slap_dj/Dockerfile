FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /site
WORKDIR /site
RUN pip install --upgrade pip
COPY requirements.txt /site/

RUN pip install -r requirements.txt
COPY . /site/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
