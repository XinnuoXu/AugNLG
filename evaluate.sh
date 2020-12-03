
#DOMAIN=taxi
#DOMAIN=train
#DOMAIN=tv
#DOMAIN=hotel
#DOMAIN=laptop
#DOMAIN=restaurant
#DOMAIN=attraction
DOMAIN=$1
DATA_TYPE=FewShotWoz

python evaluator.py --domain ${DOMAIN} --target_file results_${DOMAIN}.json --data_type ${DATA_TYPE}
