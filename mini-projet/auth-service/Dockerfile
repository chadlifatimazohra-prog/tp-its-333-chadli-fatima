
FROM python:3.9-slim


WORKDIR /app


RUN pip install flask flask-sqlalchemy flask-cors requests pyjwt

COPY . .

CMD ["python", "app.py"]