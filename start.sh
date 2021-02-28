#!/bin/sh
docker run --rm -d -p 6379:6379 --name redis redis:alpine
python3 -m hub &