#!/bin/bash
# sh imdb 1

addr="/address/of/movie_tonight_py/in/ur/system"
if [  -z "$1" ] #if no argument is provided

then  

	var=$(pwd)

	python "$addr" "$var"    
else
	
	echo "$1" #name of movie passed
	python "$addr" "$1 "

fi



