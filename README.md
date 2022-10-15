# A Django project

## Build Setup

``` bash
source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
```

### on server GUnicorn restart 
``` bash
cd summit
git pull origin main
cd /home/murod
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```
> For a detailed installation 
"How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 22.04"
[guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04).

### If some changes in server just reset
```
git reset --hard HEAD
git pull
```
