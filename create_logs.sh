#!/bin/sh

if ! [ -f "logs/requests.csv" ]; then
  touch logs/foods.csv
  echo "date,time,user,method,path,response_time,message,status_code" > logs/requests.csv
else
  echo "logs/requests.csv already exists"
fi
