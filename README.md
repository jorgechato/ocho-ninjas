# Ocho by [Jorge Chato Astrain](https://whatisjorgedoing.today)

An implementation of `dtc catalogue` for the specification of the D0010 data.

- An MPAN
- A meter serial number
    
This app is using django and django-ninja for the REST API.
It's ready to be deployed on Kubernetes.

For the monitoring of the app, we are using Prometheus and Grafana.
We assume we have a Grafana instance running and we have a Prometheus datasource configured.
For the deployment of prometheus we have a vanilla k8s yaml file under `deploy/prometheus-k8s.yml`. In future iterations we could think of using Helm.

The app will expose a `/metrics` endpoint for prometheus to scrape. We are using the `django-prometheus` package for that.

At the same time we have a `/health-check` endpoint that will be used by the k8s liveness probe.
We are using the `django-health-check` package for that. It will check the database connection and migrations.

## How to run the app

**Some assumptions:**

- You have a running postgres database with the name `ocho` and the user `ocho` with the password `ocho`.
    You can change the database name, user and password in the `settings.py` file.
- You have the required environment variables set. The k8s files are using the `secrets.yml` file to set the environment variables.
    You can also set them in the `settings.py` file. If you are using docker, you can set them in the `Dockerfile` file, or if you are runnign it locally, you can set them in the `.env` file.
    I highly recommend using the `direnv` for local environments. Please generate a secret key with `python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and set it in the `.envrc` file.
    
```bash
# .envrc file
export DEBUG=True
export SECRET_KEY='xxx'
TODO
```

### Locally

- Install the dependencies with `pip install -r requirements.txt` (preferably in a virtualenv)
    you can also use `pipenv install` if you have it installed.
- Run the migrations with `python manage.py migrate`
- Run the app with `python manage.py runserver`
- Go to `http://localhost:8000/docs` to see the API docs
    
### Docker

- Build the image with `docker build -t ocho .`
- Run the container with `docker run -p 8000:8000 jorgechato/ocho:1.0.0`
    Add as many env as required. For example: `docker run -p 8000:8000 -e DEBUG=True ocho`
- Go to `http://localhost:8000/docs` to see the API docs
    
```bash
# example
$ docker build -t jorgechato/ocho:1.0.0 .
# add as many env as required. Check the assumptions section for more info
$ docker run --rm -e DEBUG=$DEBUG -e SECRET_KEY=$SECRET_KEY jorgechato/ocho:1.0.0
```

### Kubernetes

> IMPORTANT: If you wish to deploy it in a namespace other than `default`, you will need to update the `deploy/*.yml` file.

> WARNING [1/2]: The `deploy/k8s.yml` and `deploy/prometheus-k8s.yml` file are using nginx ingress resources. If you are using a cloud provider, you will need to use the ingress controller of that provider. If you are using docker desktop, you will need to use the ingress controller of docker desktop. Please install the [controller](https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.1/deploy/static/provider/cloud/deploy.yaml) under the `docker-desktop` context.

> WARNING [2/2]: In local enviroment the `imagePullPolicy` is set to `Never`. If you are using a cloud provider, you will need to change it to `Always` or `IfNotPresent` and push the image to a registry.

- Build the image with `docker build -t jorgechato/ocho:latest .`
- Update the image name to match the `deploy/k8s.yml` files if you didn't use the same name.
- Deploy the secrets with `kubectl apply -f deploy/secrets.yml`
- Deploy the app with `kubectl apply -f deploy/k8s.yml`
- Go to `http://localhost:8000/docs` to see the API docs

**Secrets**

TODO

**Postgres**

TODO

**Prometheus**

You can spin up a prometheus instance with `kubectl apply -f deploy/prometheus-k8s.yml`

Go to `http://localhost:9090` to see the prometheus UI. Check the `Targets` tab to see if the app is up and running.

## How to run the tests

- Install the dependencies with `pip install -r requirements.txt` (preferably in a virtualenv)
    you can also use `pipenv install` if you have it installed.
- Run the tests with `python manage.py test`


## How to use the app

TODO