#!/bin/bash
if [ $# -lt 1 ]; then
  echo "Errore, devi indicare la cartella di riferimento"
  exit 2
fi

FOLDER=$1
FOLDER="$(eval pwd $FOLDER)/storage"

echo $FOLDER

vol_label=( "db_rel" "db_not_rel" "db_serial" )
vol_path_folder=()
vol_name=()

for (( i = 0; i < ${#vol_label[@]}; i++ )); do
    echo $i
    vol_path_folder[${#vol_path_folder[*]}]="$FOLDER/${vol_label[i]}/data"
    vol_name[${#vol_name[*]}]=${vol_label[i]}_data
    vol_path_folder[${#vol_path_folder[*]}]="$FOLDER/${vol_label[i]}/conf"
    vol_name[${#vol_name[*]}]=${vol_label[i]}_conf
done

# Prepared all base data, start to create dirs
n=${#vol_path_folder[@]}
for (( i = 0; i < n; i++ )); do
    mkdir -p "${vol_path_folder[i]}"
done

for (( i = 0; i < n; i++ )); do
  docker volume rm ${vol_name[i]}
  docker volume create --driver local --opt type=nfs --opt device=:${vol_path_folder[i]} ${vol_name[i]}
done
