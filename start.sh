#!/bin/sh
docker run --rm -d --network host --name redis redis:alpine
python3 -m hub &