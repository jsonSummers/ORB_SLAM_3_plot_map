#!/bin/bash

file_names=("original""ancuti2017color" "demir2023low" "islam2020fast" "li2019underwater" "sharma2023wavelength")

echo "Converting ORB SLAM CSV files to PLY"
#./convert.sh

echo "Calculating cluster information"
./cluster.sh

echo "Performing full analysis"
#./analyse.sh


echo "Processing complete."