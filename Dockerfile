FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app
RUN pip install schedule
EXPOSE 8000
CMD ["python3", "Medidor.py"]