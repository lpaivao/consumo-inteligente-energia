FROM python:3.11-slim-buster
RUN pip install schedule
EXPOSE 7324
CMD ["python3", "/src/server/ServerSocketTCP.py"]