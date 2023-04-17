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

- You have the required environment variables set. The k8s files are using the `secrets.yml` file to set the environment variables.
    You can also set them in the `settings.py` file. If you are using docker, you can set them in the `Dockerfile` file, or if you are runnign it locally, you can set them in the `.env` file.
    I highly recommend using the `direnv` for local environments. Please generate a secret key with `python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and set it in the `.envrc` file.
    
```bash
# .envrc file
export DEBUG=True
export SECRET_KEY='xxx'

# NOT required for this version
export DB_NAME='db_name'
export DB_USER='db_username'
export DB_PASSWORD='password'
export DB_HOST='db_hostname_or_ip'
export DB_PORT='db_port'
```

### Locally

- Install the dependencies with `pip install -r requirements.txt` (preferably in a virtualenv)
    you can also use `pipenv install` if you have it installed.
- Run the migrations with `python manage.py migrate`
- Run the app with `python manage.py runserver`
- Go to `http://localhost:8000/docs` to see the API docs
    
### Docker

> IMPORTANT: In order to run our application we are using django built-in server. This is not recommended for production environments. But for the sake of simplicity, we are using it.
> In a realistic scenario, we would use a WSGI server like gunicorn or uwsgi. 

- Build the image with `docker build -t ocho .`
- Run the container with `docker run -p 8000:8000 jorgechato/ocho:1.0.0`
    Add as many env as required. For example: `docker run -p 8000:8000 -e DEBUG=True ocho`
- Go to `http://localhost:8000/docs` to see the API docs
    
```bash
# example
$ docker build -t jorgechato/ocho:1.0.0 .
# add as many env as required. Check the assumptions section for more info
$ docker run --rm -e DEBUG=$DEBUG -e SECRET_KEY=$SECRET_KEY -p 8000:8000 jorgechato/ocho:1.0.0
```

### Kubernetes

> IMPORTANT: If you wish to deploy it in a namespace other than `default`, you will need to update the `deploy/*.yml` file.

> WARNING [1/2]: The `deploy/k8s.yml` and `deploy/prometheus-k8s.yml` file are using nginx ingress resources. If you are using a cloud provider, you will need to use the ingress controller of that provider. If you are using docker desktop, you will need to use the ingress controller of docker desktop. Please install the [controller](https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.1/deploy/static/provider/cloud/deploy.yaml) under the `docker-desktop` context.

> WARNING [2/2]: In local enviroment the `imagePullPolicy` is set to `Never`. If you are using a cloud provider, you will need to change it to `Always` or `IfNotPresent` and push the image to a registry.

- Build the image with `docker build -t jorgechato/ocho:1.0.0.`
- Update the image name to match the `deploy/k8s.yml` files if you didn't use the same name.
- Deploy the secrets with `kubectl apply -f deploy/secrets.yml`
- Deploy the app with `kubectl apply -f deploy/k8s.yml`
- Go to `http://localhost:8000/docs` to see the API docs

**Secrets**

K8s allows you to store sensitive information in secrets. We can use either a yml file or a command line. I prefer the command line because it's easier to automate.
And doesn't require you to store the secrets in a file, and consequently, potentially in a git repo.
If we want to use a yml file we can add it in the CI/CD pipeline but never in the repo unless we have some templating.
You can create the secrets with the following command:

```bash
# add as many env as required. Check the assumptions section for more info
# here are the ones we are using in this app
# SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
$ kubectl create secret generic ocho-secrets --from-literal=SECRET_KEY=$SECRET_KEY --from-literal=DB_NAME=$DB_NAME --from-literal=DB_USER=$DB_USER --from-literal=DB_PASSWORD=$DB_PASSWORD --from-literal=DB_HOST=$DB_HOST --from-literal=DB_PORT=$DB_PORT
```

**Postgres (for next version)**

This app uses Postgress as the database. I'm using the official Postgres image for local environments. For production environments, I would use a managed Postgres service.
We asume that postgress is already up and running. I won't go into details on how to deploy it but, as personal note, k8s is not the best place to set up a database.
AWS RDS is a good option for production environments. In my case I'm using a free database in [Render](https://render.com/).

**Prometheus**

You can spin up a prometheus instance with `kubectl apply -f deploy/prometheus-k8s.yml`

Go to `http://localhost:9090` to see the prometheus UI. Check the `Targets` tab to see if the app is up and running.

## How to run the tests

- Install the dependencies with `pip install -r requirements.txt` (preferably in a virtualenv)
    you can also use `pipenv install` if you have it installed.
- Run the tests with `python manage.py test`


## How to use the app

The first time you run it you may need to create a superuser. You can do it with `python manage.py createsuperuser`.
Check the migrations folder to see the initial data.

```bash
$ python manage.py makemigrations
$ python manage.py makemigrations meter # if you are using a different app name
$ python manage.py migrate
$ python manage.py createsuperuser
```

After running the required commands for creating a super user and the required migrations, you can go directly to the API docs at `http://localhost:8000/meter/docs` to see the API docs.
There is an admin endpoint at `http://localhost:8000/admin` where you can see the data.

To import the data from the required file, you can use the following command:

```bash
$ python manage.py importer data/DTC5259515123502080915D0010.uff
```
