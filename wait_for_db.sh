#!usr/bin/sh
# wait_for_db.sh - run by docker-compose

until nc -z $POSTGRES_HOST $POSTGRES_PORT
do
 echo Waiting... $POSTGRES_HOST
 sleep 1
done

echo Connected with $POSTGRES_USER.
