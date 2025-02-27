FROM python:3.12
LABEL authors="yuriy"
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r req.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]