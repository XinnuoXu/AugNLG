#!/bin/bash

DOMAIN=$1

sh pre_train.sh $DOMAIN
sh train.sh $DOMAIN
sh decode.sh $DOMAIN
sh evaluate.sh $DOMAIN
