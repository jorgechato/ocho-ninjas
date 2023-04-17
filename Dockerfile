FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1  
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /ocho
COPY . /ocho

# Install our requirements.
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -Ur requirements.txt

EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ./entrypoint.sh