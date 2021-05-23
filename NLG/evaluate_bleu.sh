
#DOMAIN=taxi
#DOMAIN=train
#DOMAIN=tv
#DOMAIN=hotel
#DOMAIN=laptop
#DOMAIN=restaurant
#DOMAIN=attraction
DOMAIN=$1

python txt_to_json.py ${DOMAIN}
python evaluate_bleu.py --domain ${DOMAIN} --target_file results_${DOMAIN}.json
