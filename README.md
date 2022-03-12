<!-- Music Library --># music
<!-- Use sudo in case of permission errors -->
docker-compose up

docker-compose run --rm music python manage.py migrate

docker-compose down
