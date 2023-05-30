#!/bin/bash

###############################################
#                                             #
#  Script para hacer el deploy en heroku de   #
#  un tag de un proyecto alojado en github.   #
#                                             #
#  Obs.: Ya maneja las bases de datos,        #
#  tambien genera los registros, en local  y  #
#  en produccion.                             #
#                                             #
###############################################

# Parametros desde la linea de comandos
tipoDeploy=$1

# Definimos variables para los colores de los
# echo statements
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 11`
NC=`tput sgr0`

# Descripcion: Pausar programa
# Parametros: Nada
# Retorna: Nada
pausarPrograma(){
	echo -en "${YELLOW}Presione ENTER para continuar...${YELLOW}"
	read
	echo -en ${NC}
}

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

# Descripcion: Manejo de errores
# Parametros:
#	$1 -> Mensaje del error
# Retorna: Nada
error(){
	local mensaje=$1
	echo -e "${RED}ERROR: $mensaje${RED}"
	
	# Flag del bucle
	local flag=1
	# Regex con las opciones y/n
	re='^[yn]+$'
	
	while [ $flag -eq 1 ]; 
	do
		echo -en "${YELLOW}Desea continuar con la ejecucion del programa? (y/n): ${YELLOW} ${NC}"
		read a
		
		if [[ $a =~ $re ]]; then
			if [ $a == "y" ]; then
				flag=0
			else 
				echo -e "${GREEN}Finalizando programa...${GREEN} ${NC}"
				exit 0
			fi
		else 
			echo -e "${RED}Opcion Invalida! \nDebe ingresar solo \"y\" o \"n\"${RED}"
		fi 
		
	done

	pausarPrograma
}

# Descripcion: Clona el proyecto con la direccion url recibido como parametro
# Parametro:
#	$1 -> Url del proyecto en github a clonar
#	$2 -> Direccion al directorio local en donde clonar el proyecto
#	$3 -> Nombre de la rama a clonar
# Retorna: Nada
clonar(){
	local urlProyecto=$1
	local pathDestino=$2
	local nombreRama=$3

	echo -e "${YELLOW}Clonando repositorio \"$urlProyecto\"...${YELLOW} ${NC}"	
	if git -C "$pathDestino" clone -b $nombreRama $urlProyecto; then
		echo -e "${GREEN}Repositorio remoto clonado con exito!${GREEN} ${NC}"
	else
		error "Error al clonar el repositorio remoto"	
	fi
}

# Descripcion: 	Borra el directorio local en caso de que exista el repositorio git en 
#		la direccion local dada.
# Parametro: 
#	$1 -> Path al directorio local a borrar
# Retorna: Nada
limpiarLocal(){
	local pathProyecto=$1
		
	if [ -d "$pathProyecto" ]; then
		echo -e "${YELLOW}Borrando directorio \"$pathProyecto\"${YELLOW} ${NC}"
		if rm -r --interactive=never "$pathProyecto"; then
			echo -e "${GREEN}Directorio local borrado!${GREEN} ${NC}"
		else
			error "No se pudo borrar el directorio!"
			pausarPrograma
		fi
	else 
		echo "No existe el directorio local a borrar!"
	fi
}


# Descripcion: Crear el archivo env.js en el entorno del frontend
# Parametros: 
#	$1 -> Direccion del archivo a crear
# Retorna: Nada
creandoArchivoEnv(){
	local pathArchivo=$1
	
echo "Creando archivo env.js..."
cat > "$pathArchivo/env.js" <<-EOF
const env = {
    GOOGLE_CLIENT_ID: '619211861447-4ct17vkmnl8v694j8c7pb61a2rniurrb.apps.googleusercontent.com',
}

export default env
EOF

echo "Archivo env de frontend creado!"
}

# Descripcion: Elimina los archivos de migraciones del proyecto local en el backend
# Parametros:
#	$1 -> Path al directorio raiz del proyecto
# Retorna: Nada
eliminarMigraciones(){
	local pathDirectorio=$1
	find . -path "$pathDirectorio/*/migrations/*.py" -not -name "__init__.py" -delete
}


# Descripcion: Lista las apps registradas actualmente en el proyecto
# Parametros: 
#	$1 -> Path al directorio raiz del proyecto
#	$2 -> Lista a retornar
# Retorno: Lista de valores
listarAppsBackend(){
	local pathProyecto=$1
	local -n listaRet=$2

	# Listamos todos los directorios del proyecto
	for nombreDirectorio in $(find $pathProyecto/ -maxdepth 1 -type d); do 
		#echo "Nombre del directorio: $nombreDirectorio"
		nombre="${nombreDirectorio##*/}"
		#echo "Nombre del directorio: ${nombreDirectorio##*/}"
		if [ "$nombre" != ".idea" ] && [ "$nombre" != ".git" ] && [ "$nombre" != "staticfiles" ] && [ "$nombre" != "scripts" ] && [ "$nombre" != "settings" ] && [ "$nombre" != "ProyectoScrum" ] && [ "$nombre" != "venv" ] && [ "$nombre" != "tests" ] && [ "$nombre" != "app" ] && [ "$nombre" != "fixtures" ]; then
			listaRet+=("$nombre")
		fi 
	done
}

# Descripcion: Borra la BD "postgres" y crea nuevamente con contraseña "postgres"
# Parametros: Nada
# Retorna: Nada
crearBD(){
	echo -e "${YELLOW}Recreando la base de datos...${YELLOW} ${NC}"
	. ./bd.sh
	
	echo "${GREEN}Recreando la base de datos...${GREEN} ${NC}"
	pausarPrograma
}

# Descripcion: Despliega el proyecto en el entorno de desarrollo local
# Parametros: 
#	$1 -> Path al directorio raiz del proyecto
# Retorna: Nada
deployBackendLocal(){
	local pathProyecto=$1
	
	crearBD
	
	echo -e "${YELLOW}Creando el entorno...${YELLOW} ${NC}"
	
	# Eliminando el entorno
	if rm -r "$pathProyecto/venv"; then
		echo ""
	else
		echo ""
	fi
	
	
	# Creando el entorno
	echo -e "${YELLOW}Creando el entorno venv...${YELLOW} ${NC}"
	
	# Verificamos que si retorna cero, se muestre el mensaje de error
	if python3 -m venv "$pathProyecto/venv"; then
		echo -e "${GREEN}Entorno venv creado con exito${GREEN} ${NC}"			
	else
		error "El entorno no pudo ser creado correctamente!!"
	fi 

	
	# Eliminamos todas las migraciones: 
	eliminarMigraciones $pathProyecto

	# Lista de Apps 
	listaApps=()
	listarAppsBackend $pathProyecto listaApps

	#echo "Imprimiendo lista de Apps: ${listaApps[@]}"
	pausarPrograma

gnome-terminal -- sh -c '
	cd $1
	listaApps=$@
#	echo "Argumentos: $listaApps"
	listaApps="${listaApps#* }"
#	echo "Lista de aplicaciones: $listaApps"
	chmod +x ./venv/bin/activate
	. ./venv/bin/activate
	pip install -r requirements.txt
	for nombreApp in $listaApps; do
		python3 manage.py makemigrations "$nombreApp"
	done
	python3 manage.py makemigrations
	for nombreApp in $listaApps; do
		python3 manage.py migrate "$nombreApp"
	done
	python3 manage.py migrate
	python3 manage.py runserver' sh "$pathProyecto" "${listaApps[@]}"
	
	echo -e "${RED}Espere a que todas las migraciones sean creadas!${RED} ${NC}"
pausarPrograma
	
	# ???Operar en la BD (flush/drop) DONE
	# Crear las migraciones DONE 
	# Aplicar las migraciones DONE
	# Ejecutar el server (en otro subshell para que no interfiera con el server del front) DONE
}


# Descripcion: Despliega el proyecto en el entorno de desarrollo remoto
# Parametros:
#	$1 -> Path al directorio donde se encuentra el repositorio local a desplegar
#	$2 -> Nombre de la app a desplegar
# Retorna: Nada
deployBackendHeroku(){
	# Parametros
	local pathDirectorio=$1
	local nombreApp=$2
	
	echo -e "{$YELLOW}Reseteando la base de datos... {$YELLOW}"
	if heroku pg:reset DATABASE -c $nombreApp -a $nombreApp; then
		echo -e "{$GREEN}Reset de la base de datos realizada con exito{$GREEN} {$NC}"
		pausarPrograma
	else
		error "No se pudo resetear la base de datos de produccion!" 
	fi
	

	# Creando el entorno
	echo -e "${YELLOW}Creando el entorno venv...${YELLOW} ${NC}"
	# Verificamos que si retorna cero, se muestre el mensaje de error
	if python3 -m venv "$pathDirectorio/venv"; then
		echo -e "${GREEN}Entorno venv creado con exito${GREEN} ${NC}"			
	else
		error "El entorno no pudo ser creado correctamente!!"
	fi 
	
	# Borrando bd local
	#crearBD
	
	
	# Eliminamos todas las migraciones: 
	eliminarMigraciones $pathDirectorio

	# Lista de Apps 
	listaApps=()
	listarAppsBackend $pathDirectorio listaApps
	
	# Cargamos las migraciones a la bd de heroku
	
gnome-terminal -- sh -c '
	cd $1
	listaApps=$*

	chmod +x ./venv/bin/activate
	. ./venv/bin/activate
	pip install -r requirements.txt
	echo "Lista de apps: $listaApps"
	echo "Creando migraciones..."
	i=0
	for nombre in $listaApps; do
		if [ $i -ne 0 ]; then
			python3 manage.py makemigrations "$nombre"
		fi
		i=$((i+1))
	done
	python3 manage.py makemigrations
	
	j=0
	for nombre in $listaApps; do
		if [ $j -ne 0 ]; then
			python3 manage.py migrate "$nombre"
		fi
		j=$((j+1))
	done
	python3 manage.py migrate	
	echo "Proceso finalizado!"
	echo "Presione enter para cerrar esta ventana!"
	read d' sh "$pathDirectorio" ${listaApps[@]}


	cd "$pathDirectorio"
#	chmod +x ./venv/bin/activate
#	. ./venv/bin/activate
#	pip install -r requirements.txt
#	
#	echo "Lista de apps: ${listaApps[@]}"
#	echo "Creando migraciones..."
#	for nombre in ${listaApps[@]}; do
#		python3 manage.py makemigrations "$nombre"
#	done
#	python3 manage.py makemigrations
#	
#	echo "Aplicando migraciones..."
#	for nombre in ${listaApps[@]}; do
#		python3 manage.py migrate "$nombre"
#	done
#	python3 manage.py migrate	


	if heroku git:remote -a $nombreApp; then
		echo -e "${GREEN}Operacion de CHECKOUT al main realizada con exito ${GREEN} ${NC}"
		pausarPrograma
	else
		error "No se pudo hacer checkout al heroku:main"
	fi
	
	if git push -f heroku HEAD:refs/heads/master; then
		echo -e "${GREEN}Operacion de PUSH a Heroku realizada con exito${GREEN} ${NC}"
		pausarPrograma
	else
		error "No se pudo hacer push a heroku!"
	fi
	
	cd ..
}

# Descripcion: Despliega el proyecto frontend en el entorno local
# Parametros:
#	$1 -> Path al directorio local
# Retorna: Nada
deployFrontendLocal() {
# Parametros
local pathProyecto=$1

gnome-terminal -- sh -c "cd $pathProyecto; npm i; npm run serve"

pausarPrograma
}


# Descripcion: Despliega el proyecto frontend en el entorno remoto
# Parametros:
# 	$1 -> Path al directorio remoto
# Retorna: Nada
deployFrontendFirebase() {
	local pathDirectorio=$1


gnome-terminal -- sh -c '
	cd $1
	npm i
	npm run build

	firebase -c firebase.json deploy
	echo "Proceso finalizado!"
	echo "Presione enter para cerrar esta ventana!"
	read d' sh "$pathDirectorio"

}

# Descripcion: Obtiene del repositorio remoto el tag seleccionado y cambiamos
#		el entorno de trabajo local en el proyecto del backend
# Parametros: 
#	$1 -> Nombre del Tag elegido para hacer el checkout
#	$2 -> Path al directorio en donde se encuentra el repositorio git local.
# Retorna: Nada
operandoGithubBackend(){
	# Parametros
	local nombreTag=$1
	local pathProyecto=$2	
	
	# Cambiamos a la rama principal (origin/main)
	#if git -C "$pathProyecto" checkout master; then
	#	echo -e "${GREEN}Operacion de CHECKOUT al main realizada con exito ${GREEN}"
	#	pausarPrograma
	#else
	#	error "No se pudo hacer CHECKOUT al main del proyecto!"
	#fi

	
	# Actualizamos el proyecto
	#if git -C "$pathProyecto" pull; then
	#	echo -e "${GREEN}Operacion de PULL realizada con exito ${GREEN}"
	#	pausarPrograma
	#else
	#	error "No se pudo hacer PULL del proyecto!"
	#fi

	# Checkout al TAG	
	if git -C "$pathProyecto" checkout -f tags/"$nombreTag"; then
		echo -e "${GREEN}Checkout realizado con exito!${GREEN} ${NC}"
		pausarPrograma
	else
		error "No se pudo hacer CHECKOUT al tag \"$nombreTag\""
	fi
 
}

# Descripcion: Obtiene del repositorio remoto el tag seleccionado y cambiamos
#		el entorno de trabajo local en el proyecto del frontend
# Parametros: 
#	$1 -> Nombre del Tag elegido para hacer el checkout
#	$2 -> Path al directorio en donde se encuentra el repositorio git local.
# Retorna: Nada
operandoGithubFrontend(){
	# Parametros
	local nombreTag=$1
	local pathProyecto=$2	
	
	# Cambiamos a la rama principal (origin/main)
	#if git -C "$pathProyecto" checkout main; then
	#	echo -e "${GREEN}Operacion de CHECKOUT al main realizada con exito ${GREEN}"
	#	pausarPrograma
	#else
	#	error "No se pudo hacer CHECKOUT al main del proyecto!"
	#fi

	
	# Actualizamos el proyecto
	#if git -C "$pathProyecto" pull; then
	#	echo -e "${GREEN}Operacion de PULL realizada con exito ${GREEN}"
	#	pausarPrograma
	#else
	#	error "No se pudo hacer PULL del proyecto!"
	#fi

	# Checkout al TAG	
	if git -C "$pathProyecto" checkout -f tags/"$nombreTag"; then
		echo -e "${GREEN}Checkout realizado con exito!${GREEN} ${NC}"
		pausarPrograma
	else
		error "No se pudo hacer CHECKOUT al tag \"$nombreTag\""
	fi
 
}

# Descripcion: Agrega el fixture de django seleccionado, a la BD en el entorno local.
#		Aun no se pobla la base de datos, sino que solo opera para agregar
#		el archivo bd.json al directorio en donde deberia ubicarse.
# Parametros: 
#	$1 -> Path al proyecto de backend
#	$2 -> Path al bd.json seleccionada
# Retorno: Nada
cargarFixtureLocal(){
	local pathProyecto=$1
	local pathBD=$2
	
	# Eliminamos el directorio de fixtures del proyecto local (existe solo en iteracion5 en adelante)
	rm -r "$pathProyecto/fixtures"
	# Creamos una carpeta llamada /fixtures en el entorno local
	if mkdir "$pathProyecto/fixtures"; then
		echo "Directorio de fixtures creado..."
	else
		error "No se pudo crear el directorio de fixtures"
	fi
	
	# Copiamos el archivo bd.json al directorio creado
	# cp [...file/directory-sources] [destination]
	if cp "$pathBD" "$pathProyecto/fixtures"; then
		echo "Fixture agregado al proyecto"
	else
		error "No se pudo agregar el fixture al proyecto"
	fi 
	
	# Agregamos los cambios (si el proyecto esta en produccion, sino, no es necesario)
 	if [ "$tipoDeploy" == "prod" ]; then
		if git -C "$pathProyecto" add "./fixtures/prod.json"; then
			echo "Cambios de BD agregados"
		else
			error "No se pudo agregar cambios de BD"
		fi
		
		# Guardando cambios
		if git -C "$pathProyecto" commit -m "BD.json"; then
			echo "Cambios de BD guardados"
		else
			error "No se pudo guardar cambios de BD"
		fi
	fi	
}

# Descripcion: Pobla la BD local
# Parametros:
#	$1 -> Path al directorio local del proyecto
# Retorna: Nada
cargarBDLocal(){
	local pathProyecto=$1

gnome-terminal -- sh -c '
	cd $1
	echo "Iniciando carga de datos..."
	chmod +x ./venv/bin/activate
	. ./venv/bin/activate
	python3 "manage.py" loaddata "./fixtures/prod.json"
	echo "Proceso finalizado!"
	echo "Presione enter para cerrar esta ventana!"
	read d' sh "$pathProyecto"
}

# Descripcion: Pobla la BD remota
# Parametros:
#	$1 -> Path al directorio local del proyecto
# Retorna: Nada
cargarBDHeroku(){
	local pathProyecto=$1
	
	echo -e "${YELLOW}Cargando datos en la BD de heroku...${YELLOW} ${RED}\nVerifique que todas las migraciones hayan sido aplicadas, luego continue! ${RED} ${NC}"
	pausarPrograma
	cd $pathProyecto
	heroku run python3 manage.py loaddata ./fixtures/prod.json
	cd ..
}


# Descripcion: Despliega el menu del sistema
# Parametros:
# 	$1 -> Valor a retornar con el nombre del tag del back (por referencia)
#	$2 -> Valor a retornar con el nombre del tag del front (por referencia)
#	$3 -> Valor a retornar con el path del bd.json guardado en el entorno local (por referencia)
#	$4 -> Valor a retornar con la respuesta y/n para poblar la BD (por referencia)
# Retorno: 
#	$1 con la opcion seleccionada para el backend
#	$2 con la opcion seleccionada para el frontend
#	$3 con la opcion seleccionada para la base de datos
#	$4 con la opcion seleccionada para poblar la base de datos
menu(){
	# Parametros
	local -n retBackend=$1
	local -n retFrontend=$2
	local -n retBD=$3
	local -n retPoblar=$4
	
	# Lista con el nombre de los TAGS del backend
	listaNombreBackend=("Hito1" "Iteracion2" "Iteracion3" "Iteracion4" "Iteracion5" "Iteracion6")
	# Lista con el nombre de los TAGS del frontend
	listaNombreFrontend=("iteracion1" "iteracion2" "iteracion3" "iteracion4" "iteracion5" "iteracion6")
	# Lista con el path de cada BD (uno por cada iteracion)
	listaPathBD=("iteracion1/prod.json" "iteracion2/prod.json" "iteracion3/prod.json" "iteracion4/prod.json" "iteracion5/prod.json" "iteracion6/prod.json")
	
	# Flag para terminar el bucle del menu
	local flag=1
	while [ $flag -eq 1 ]; 
	do
		clear
		echo "###################################################"
		echo "#                                                 #"
		echo "#  Sistema de Administracion de Proyectos Agiles  #"
		echo "#                                                 #"
		echo "###################################################"
		echo "#                                                 #"
		echo "#  Las siguientes opciones son las distintas      #"
		echo "#  alternativas de versiones del proyecto a ser   #"
		echo "#  desplegadas en el server remoto o local        #"
		echo "#                                                 #"
		echo "###################################################"
		echo
		echo "Seleccione una opción:"
		echo "1. Iteracion 1"
		echo "2. Iteracion 2"
		echo "3. Iteracion 3"
		echo "4. Iteracion 4"
		echo "5. Iteracion 5"
		echo "6. Iteracion 6"
		echo "7. Cancelar"
		echo -n "Opcion -> "
		read op
		
		# Verificamos el input sea un numero en el intervalo 
		# requerido
		re='^[1-7]+$'
		if [[ $op =~ $re ]] ; then	
			if [ $op -eq 7 ]; then
				echo -e "${GREEN}Cancelando operacion!${GREEN} ${NC} \n\nFinalizando programa"
				echo -e "${YELLOW}Presione cualquier tecla para continuar...${YELLOW} ${NC}"
				read
				exit 0
			else
				# Guardamos el valor de retorno
				retBackend=${listaNombreBackend[($op-1)]}
				retFrontend=${listaNombreFrontend[($op-1)]}
				retBD=${listaPathBD[($op-1)]}
				flag=0
			fi
		else
			error "La opción seleccionada no existe! \nIntente nuevamente"
		fi
	done
	
	# Flag del bucle
	local flag2=1
	# Regex con las opciones y/n
	local re='^[yn]+$'
	
	while [ $flag2 -eq 1 ]; 
	do
		echo -en "${YELLOW}Desea poblar la BD con los registros de prueba?\nEsta operacion borra todos los registros actuales! (y/n): ${YELLOW} ${NC}"
		read a
		
		if [[ $a =~ $re ]]; then
			retPoblar=$a
			flag2=0
		else 
			echo -e "${RED}Opcion Invalida! \nDebe ingresar solo \"y\" o \"n\"${RED}"
		fi 
		
	done
}

# Para operar con github, se debe ingresar la cuenta y el token de acceso
# generado desde la web.
# TO-DO: Automatizar esta parte (algun archivo externo donde cada uno agrega
# el token y el username de github a ser importados a este programa)

# TO-DO: Avisar al usuario que para el checkout se hace un --force checkout

# Variables
pathProyectoBackend="./ProyectoScrum"
pathProyectoFrontend="./ProyectoScrumFrontend"
pathProyectoBD="./fixtures"
nombreApp="proyectoscrumgrupo5"

# Mostramos el menu de inicio
opcionBackend=""
opcionFrontend=""
opcionBD=""
opcionPoblar=""
menu opcionBackend opcionFrontend opcionBD opcionPoblar

echo "La opcion seleccionada para el backend: $opcionBackend"
echo "La opcion seleccionada para el frontend: $opcionFrontend"
echo "La opcion seleccionada para el bd: $opcionBD"
echo "La opcion seleccionada de poblar y/n: $opcionPoblar"

# Borramos los directorios de proyectos y clonamos nuevamente
limpiarLocal "./ProyectoScrum"
limpiarLocal "./ProyectoScrumFrontend"

clonar "https://github.com/arturojeich/ProyectoScrum.git" "." "master"
clonar "https://github.com/JessiProgram/ProyectoScrumFrontend.git" "." "dev2"

# Obteniendo el tag seleccionado del menu
operandoGithubBackend $opcionBackend $pathProyectoBackend

# ./ProyectoScrumFrontend/src/configs
creandoArchivoEnv "./ProyectoScrumFrontend/src/configs"

# La iteracion 1 no se encontraba desplegada en el frontend!!
if [ "$opcionFrontend" != "iteracion1" ]; then
	# Obteniendo el tag seleccionado del menu
	operandoGithubFrontend $opcionFrontend $pathProyectoFrontend
fi

# Inicio del programa
# Verificamos el tipo de deploy a realizar
if [ "$tipoDeploy" == "dev" ]; then
	# Iniciando el deploy en local
	echo -e "${YELLOW}Iniciando despliegue del proyecto en el entorno local...${YELLOW} ${NC}"

	# La iteracion 1 no se encontraba desplegada en el frontend!!
	if [ "$opcionFrontend" != "iteracion1" ]; then
		echo -e "${YELLOW}Iniciando despliegue del frontend...${YELLOW} ${NC}"
		deployFrontendLocal $pathProyectoFrontend
	fi

	# Editamos el entorno (todos los tags del backend siempre apuntan a production)
	editarManagepy $pathProyectoBackend "local"
	
	if [ "$opcionPoblar" == "y" ]; then
		# Cargar la BD en entorno local
		cargarFixtureLocal $pathProyectoBackend "$pathProyectoBD/$opcionBD"
	fi

	
	# Deploy en local
	echo -e "${YELLOW}Iniciando despliegue del backend...${YELLOW} ${NC}"
	deployBackendLocal $pathProyectoBackend
	
	if [ "$opcionPoblar" == "y" ]; then
		echo "${YELLOW}Poblando la BD con los registros de prueba...${YELLOW} ${NC}"
		cargarBDLocal $pathProyectoBackend
		pausarPrograma
	fi
	echo -e "${GREEN}Despliegue del entorno de desarrollo finalizado!${GREEN} ${NC}"

		
elif [ "$tipoDeploy" == "prod" ]; then
	
	# Para la ejecucion en el entorno de desarrollo, borramos el venv/ si es que se encuentra de algun
	# deploy local que se realizo anteriormente
	
	# Deploy en firebase
	# La iteracion 1 no se encontraba desplegada en el frontend!!
	if [ "$opcionFrontend" != "iteracion1" ]; then
		echo -e "${YELLOW}Iniciando despliegue del Frontend (en Firebase)...${YELLOW} ${NC}"
		deployFrontendFirebase $pathProyectoFrontend
	fi	
	
	# Eliminando el entorno
	rm -r "$pathProyectoBackend/venv"
	
	if [ "$opcionPoblar" == "y" ]; then
		# Cargar la BD en entorno local
		cargarFixtureLocal $pathProyectoBackend "$pathProyectoBD/$opcionBD"
	fi
	
	
	# Deploy en heroku
	echo -e "${YELLOW}Iniciando despliegue del backend (en Heroku)...${YELLOW} ${NC}"
	deployBackendHeroku $pathProyectoBackend $nombreApp
	
	if [ "$opcionPoblar" == "y" ]; then
		echo ""
		cargarBDHeroku $pathProyectoBackend
	fi
	echo -e "${GREEN}Despliegue del entorno de produccion finalizado!${GREEN} ${NC}"

else
	error "Opcion de deploy invalida!!"
fi	


