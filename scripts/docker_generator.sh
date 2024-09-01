#!/bin/bash

read -p "Ingrese el nombre del archivo a crear: " file_name
read -p "Ingrese el número de clientes: " number

python3 scripts/docker_generator/main.py --file "$file_name" --number "$number"
