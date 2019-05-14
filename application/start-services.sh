#!/bin/bash

sudo docker-compose pull

sudo docker-compose run -d log_generator
sudo docker-compose run -d --name rabbitmq_service rabbitmq_service
sudo docker-compose run -d rabbit_worker
sudo docker-compose run -d --name elasticsearch_service elasticsearch_service
sudo docker-compose run -T --name client_container client

sudo docker exec -it client_container /bin/bash
