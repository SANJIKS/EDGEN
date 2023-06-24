FROM python:3.10 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic

COPY . .

CMD [ "python", "manage.py migrate" ]
