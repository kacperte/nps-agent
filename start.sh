#!/bin/bash
sleep 15
yoyo apply -b
uvicorn main:app --host 0.0.0.0 --reload