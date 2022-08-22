##############################################
#                                            #
# Script para la generacion de usuarios de   #
# prueba para prueba del proyecto a nivel    #
# local.                                     #
##############################################


# Creamos un usuario de prueba
#   -> $1 : Email
#   -> $2 : Nombres
#   -> $3 : Apellidos
#   -> $4 : Contraseña
#   -> $5 : Rol
#   -> $6 : Username
crearUsuario(){
  email=$1
  nombres=$2
  apellidos=$3
  contrasenha=$4
  rol=$5
  username=$6
  echo ""
  echo "---------------------------------"
  echo "Usuario a registrar:"
  echo "Email: $email"
  echo "Nombres: $nombres"
  echo "Apellidos: $apellidos"
  echo "Contraseña: $contrasenha"
  echo "Rol: $rol"
  echo "Rol: $username"
# Abrimos el shell de python
python3 manage.py shell<<-CONFIG
	from django.contrib.auth import get_user_model
	UserMan=get_user_model()
	user=UserMan.objects.create_user("$email", password="$contrasenha", nombres="$nombres", apellidos="$apellidos", rol=$rol, username="$username")
	user.save()
	exit()
	CONFIG
	echo "---------------------------------"
}

echo "Iniciando Script..."

# Creamos usuarios
crearUsuario 'usuario1@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password1' 'None' 'username1'
crearUsuario 'usuario2@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password2' 'None' 'username2'
crearUsuario 'usuario3@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password3' 'None' 'username3'
crearUsuario 'usuario4@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password4' 'None' 'username4'
crearUsuario 'usuario5@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password5' 'None' 'username5'
crearUsuario 'usuario6@gmail.com' 'Nombres 1 y 2' 'Apellidos 1 y 2' 'password6' 'None' 'username6'

echo "Finalizando Script..."
