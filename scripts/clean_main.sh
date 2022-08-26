#!/bin/bash

# git-clean-main 
# Borra directorios de la rama actual

# Path a los archivos/directorios a borrar
# Ejemplo Archivos: 
#			directorio/nombreArchivo.txt
#			nombreArchivo.txt (al mismo nivel que el script).
# Ejemplo Directorios:
#			directorioNombre (directorio al mismo niveo que el script).
#			directorioPadre/directorioHijo (Padre al mismo nivel que el script).

# Lista de directorios/archivos a eliminar
listaPaths=(
"./.pytest_cache"
"./documentacion"
)

# Valor 1(false)/0(true) haces el push a master con los cambios
actualizarBranch=0 # Por defecto, False

# Branch a la cual subir los cambios
branch="master"

# Eliminar directorios desde el path actual
eliminarLista() {
	lista=("$@")
	echo "-------------------------------------------------"
	echo ""
	echo "ELIMINANDO..."
	echo ""
	for ((a=0;a<${#lista[@]};a++))
	do		
		if [[ -d ${lista[$a]} ]]; then
			echo "Borrando Directorio ${lista[$a]}"
			rm -r "${lista[$a]}"
		else
			if [[ -f ${lista[$a]} ]]; then	
				echo "Borrando Archivo ${lista[$a]}"
				rm ${lista[$a]}
			else 
				echo "${lista[$a]} || No se puede procesar/no existe."
			fi
		fi
	done
	echo ""
	echo "-------------------------------------------------"

}

procesarGit() {
	branchName=$1
	echo "ACTUALIZANDO REPOSITORIO"
	echo ""
	echo "Actualizando Local (commit de cambios)"
	git commit . -m "Cleaning up production"# Remueve el directorio duplicado
	echo "Actualizando remoto (push a $branchName)"	
	git push origin "$branchName"
}

echo "-------------------------------------------------"
echo "-------------------------------------------------"
echo "-              Iniciando Script...              -"
echo "-------------------------------------------------"
echo "-------------------------------------------------"

echo ""
if [[ $actualizarBranch -eq 0 ]]; then	
	# Accedemos a la rama branch
	echo "Checkout a $branch"
	git checkout -b master
else
	echo "No se cambia a branch main"
fi
echo ""

echo "-------------------------------------------------"
echo "-------------------------------------------------"
echo "-          Procesando lista a eliminar...       -"
echo "-------------------------------------------------"
# Eliminando archivos/directorios de la lista
eliminarLista "${listaPaths[@]}" #valorRetorno

echo "-------------------------------------------------"
echo "-               Operaciones en git...           -"
echo "-------------------------------------------------"
echo "-------------------------------------------------"
echo ""
if [[ $actualizarBranch -eq 0 ]]; then	
	# Guardando los cambios en el repositorio (origin>master, por defecto)
	procesarGit "$branch"	
else
	echo "NO SE ACTUALIZA EL REPOSITORIO"
fi
echo ""
echo "-------------------------------------------------"
echo "Fin del script"

