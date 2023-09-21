### Deploy and start project on AWS Ubuntu instance
* **Clone project from git repository**
```
git clone "your_repos_ssh_or_http_url"
```
Moving to project dir 
```
cd porject_dir
```
* **Installing docker in ubuntu 20/22 instance** 
```
sudo apt update && sudo apt upgrade -y
sudo apt install ca-certificates curl gnupg lsb-release unzip
```
Add Dockers GPG key
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
Add official docker repo
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) 
stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```
Installing docker
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Adding user to docker group
```
sudo usermod -aG docker $USER
id $USER
newgrp docker
```
Installing docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Checking docker and docker-compose
```
docker run hello-world
docker-compose --version
```

* **Running docker containers**
```
docker-compose up --build -d
```
Collecting staticfiles
```
docker-compose exec web python manage.py collectstatic --no-input
```
Creating superuser
```
docker-compose exec web python manage.py createsuperuser
```

### Running project local

* **Clone project from git repository**
```
git clone "your_repos_ssh_or_http_url"
```
Moving to project dir, creating virtual environment and install packages
```
cd medical
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Installing Postgres, cause we need to create database and user
```
sudo apt-get install libpq-dev postgresql postgresql-contrib
```
Entering postgres
```
sudo -u postgres psql
```
in PSQL
```
CREATE DATABASE db_name;
CREATE USER your_user WITH PASSWORD 'your_user';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'Asia/Almaty';
GRANT ALL PRIVILEGES ON DATABASE db_name TO your_user;
\q

```
Making migrations, createsuperuser and running the server at localhost:8000/
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

```
### Dump and load data
```
python3 manage.py dumpdata --indent=4 --exclude auth.permission --exclude contenttypes > db.json
python3 manage.py loaddata db.json



