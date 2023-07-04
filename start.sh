#!/bin/bash
sleep 10
yoyo apply -b
uvicorn main:app --host 0.0.0.0 --reload