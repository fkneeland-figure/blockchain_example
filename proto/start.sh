#!/bin/bash
docker build -t proto:latest .
docker run -d -p 5000:5000 proto