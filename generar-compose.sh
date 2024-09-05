#!/bin/bash

echo "Nombre del archivo de salida: $1"
echo "Cantidad de clientes: $2"

python3 scripts/docker_generator/main.py --file "$1" --number "$2"
