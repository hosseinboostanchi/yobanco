#!/bin/bash

source ./Yobancoconfig.sh

curl --data "token=$TOKEN" $BASE_URL/q/generalstat/