
FROM python:3.9
 
ENV socia_env

WORKDIR /social_media_task

COPY . /social_media_task/

RUN pip install --no-cache-dir -r req.txt

EXPOSE 8000

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
