#!/bin/bash

declare -a StringArray=( "sgd_banks" "sgd_buses" "sgd_calendar" "sgd_events" "sgd_flights" "sgd_homes" "sgd_hotels" "sgd_media" "sgd_movies" "sgd_music" "sgd_rentalcars" "sgd_restaurants" "sgd_ridesharing" "sgd_services" "sgd_travel" "sgd_weather" )
for model in ${StringArray[@]};
do
	./qualitative_sgd.sh ${model}
done
