#!/bin/bash
##############################################
#                                            #
# Script para cargar la BD con los datos de  #
# prueba.                                    #
##############################################

echo "Borrando datos de la BD..."

#python3 manage.py flush<<-Inicio
#yes
#Inicio

python3 manage.py flush

echo "Cargando database..."
python3 ./manage.py loaddata ./fixtures/bd.json
