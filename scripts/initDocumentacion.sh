##################################################
#      Comandos para crear la documentacion      #
##################################################

# Crea el directorio $pathActual/$nombreDirectorio
crearDirectorio(){
	pathActual=$1
	nombreDirectorio=$2
	local -n valorRet=$3
	echo "Creando $pathActual/$nombreDirectorio"
	mkdir "$pathActual/$nombreDirectorio"
	if [ -d "$pathActual/documentacion" ]
	then 
		echo "Directorio /$nombreDirectorio creado con exito!!"
		valorRet=0
	else 
		echo "El /$nombreDirectorio no pudo ser creado!!!"
		valorRet=1							
	fi	
}

# Verificar si el directorio documentacion/ existe 
# o no.
# Recibe:
#	- $1 -> Path al directorio a crear
#	- $2 -> Nombre del directorio a crear
#	- $3 -> Booleano
#		1 -> Directorio no existe/no fue creado
#		0 -> Directorio existe/fue creado
reiniciarDirectorio() {
	pathActual=$1
	nombreDirectorio=$2
	local -n valorRet=$3
	if [ -d "$pathActual/$nombreDirectorio" ]
	then
		echo "El directorio $pathActual/$nombreDirectorio ya existe"
		echo "Eliminando..."
		rm -r "$pathActual/$nombreDirectorio"
		echo "Creando directorio..."
		crearDirectorio $pathActual $nombreDirectorio valorRet
		valorRet=0
	else 
		echo "El directorio $pathActual/$nombreDirectorio no existe"
		crearDirectorio $pathActual $nombreDirectorio valorRet
	fi
}

# Instala Sphinx con todas las configuraciones
# Parametros:
#	-> $1 : Path al directorio docs/
#	-> $2 : Nombre directorio docs/
#	-> $3 : Nombre proyecto
#	-> $4 : Author proyecto
#	-> $5 : Version proyecto
#	-> $6 : Lenguaje
instalandoSphinx() {
	directorio="$1/$2"
	nombreProyecto=$3
	autores=$4
	version=$5
	lenguaje=$6
	
	# Instalando sphinx en directorio root del proyecto
	pip install sphinx
	
	cd "$directorio" 
	
	# Inicializando Sphinx en el directorio /documentacion 	
	sphinx-quickstart<<-CONFIG
		n
		$nombreProyecto
		$autores
		$version
		$lenguaje
	CONFIG
	
	cd ..
	
}


# Agrega configuracion al archivo conf.py
# Parametros:
#	-> $1 : path al archivo conf.py 
#	-> $2 : Encabezado a agregar
#	-> $3 : ''ext1', 'ext2', 'ext3', ...'
# -> $4 : Tema de página
editarConfpy(){
	pathArchivo=$1
	encabezado=$2
	extensiones=$3
  tema=$4

	# Agregando encabezado
	sed -i "1i$encabezado" "$pathArchivo/conf.py"
	
	# Agregando extension
	sed -i -e "s/extensions = \[\]/extensions = \[$extensiones\]/g" "$pathArchivo/conf.py"

	# Agregando theme
  sed -i -e "s/'alabaster'/'$tema'/g" "$pathArchivo/conf.py"

}



continuar=0
# Iniciando programa
reiniciarDirectorio "." "documentacion" continuar

if [ $continuar -eq 0 ]
then 
	echo "Instalando sphinx..."
 	instalandoSphinx "." "documentacion" "Proyecto Scrum" "Grupo 5" "1.0" "es"
	
	# Agregando configuraciones al conf.py
	# Definiendo el encabezado (necesario para tener los $path actuales, funciones del sistema
	# operativo y configuraciones del proyecto de django
	encabezado="import os\nimport sys\nimport django\nsys.path.insert(0, os.path.abspath('..'))\nos.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'\ndjango.setup()\n"
	# Definiendo extensiones
	extensions="'sphinx.ext.autodoc'"
	# Definiendo tema
	tema="sphinx_rtd_theme"
	editarConfpy './documentacion' "$encabezado" $extensions $tema

  # Actualizamos el index
  cd "./documentacion"

  # Actualizamos el index.rst con los modulos del proyecto
  sed -i 's/:caption: Contents:/&\n   modules/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   sprints/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   usuarios/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   tests/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   settings/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   roles/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   historiasDeUsuario/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   proyectos/' './index.rst'
  sed -i 's/:caption: Contents:/&\n   soportepermisos/' './index.rst'
  sed -i 's/:caption: Contents:/&\n/' './index.rst'
	
else
	echo "No instalamos sphinx."
fi

echo "Fin del script."
