#!/bin/sh
docker run --rm -d -p 6379:6379 -v /redis:/data --name redis-hub redis
python3 -m hub &