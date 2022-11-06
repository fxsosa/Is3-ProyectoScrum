#!/bin/bash
#######################################
#                                     #
# Script para hacer el deploy del     #
# proyecto                            #
# Parametros:                         #
# 1. El string prod/dev               #
#######################################

# Agregamos los permisos a los scripts
chmod +x ./scripts/cargar_bd.sh

# Agrega configuracion al archivo conf.py
# Parametros:
# $1 -> Direccion del archivo
# $2 -> Opcion (string prod/dev)
editarManagepy(){
	pathArchivo=$1
  opcion=$2

	# Agregando extension
	sed -i -e "s/settings\..*$/settings\.$opcion\')/g" "$pathArchivo/manage.py"
}

# Abrir en firefox/google chrome
# Parametros:
# 1. URL de la web
abrirProyecto(){
  url=$1

  temp1=$(firefox --version)
  temp2=$('google-chrome' --version)

  if [[ "$temp1" =~ "Mozilla Firefox " ]]; then
    firefox $url
  elif [[ "$temp2" =~ "Google Chrome ".* ]]; then
    'google-chrome' $url
  fi

}

# Ejecuta el front en local
front-dev(){
    direccionFront=$1

    cd $direccionFront
    npm run build
    firebase deploy
    npm i
    npm run serve

}

# Ejecutar en el backend
backend(){
  # Conf. del proyecto backend
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver
}
# Trae la version del master
configurarGit(){
  echo ""
}

# Opcion para el deploy
opcion=$1

if [ "$opcion" == "prod" ]; then
    echo "Deploy de entorno de produccion"

    editarManagepy "." "production"
    source ./scripts/cargar_bd.sh


elif [ "$opcion" == "dev" ]; then
    echo "Deploy de entorno de desarrollo"
    editarManagepy "." "local"
    source ./scripts/cargar_bd.sh

    #backend & front-dev "../ProyectoScrum-Front" && fg

    #echo "Abriendo url"
    #abrirProyecto "http://localhost:8080/"

else
    echo "Opcion de deploy invalida!"
fi
