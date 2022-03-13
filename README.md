<!-- Music Library --># music
<!-- Use sudo in case of permission errors -->
# To run with docker
```
docker-compose build (run for any changes made in the code)

docker-compose up

docker-compose run --rm music python manage.py migrate

docker-compose down

```

songs -postman-collection.json file under the current directory has all the api endpoints for local and prod environments (https://music-poc-ak.herokuapp.com/)

**Note**: Use postman collections to check APIs.

---

# To run locally without docker

#Create a virtual environment to isolate our package dependencies locally

```
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

pip install -r requirements.txt

Change the settings.py to use requiste database and its credentials

python manage.py migrate  # migrate changes to your local db

python manage.py test # to run tests

python mange.py runserver <port_number>

```
