#!/usr/bin/env sh

# stop containers if they are still running
if docker ps | grep -q "clean-marine"; then
    echo "Stopping clean-marine containers"
    docker compose down
fi

# remove containers if they still exist
if docker ps -a | grep -q "clean-marine-django-1"; then
    docker rm clean-marine-django-1 > /dev/null
    echo "Cleaned up container clean-marine-django-1"
fi

if docker ps -a | grep -q "clean-marine-selenium-1"; then
    docker rm clean-marine-selenium-1 > /dev/null
    echo "Cleaned up container clean-marine-selenium-1"
fi

# remove image if it still exists
if docker images | grep -q "clean-marine"; then
    docker image rm clean-marine-django > /dev/null
    echo "Cleaned up image clean-marine-django"
fi

# remove network if it still exists
if docker network ls | grep -q "clean-marine_default"; then
    docker network rm clean-marine_default > /dev/null
    echo "Cleaned up network clean-marine_default"
fi

# recreate image and containers
docker compose up