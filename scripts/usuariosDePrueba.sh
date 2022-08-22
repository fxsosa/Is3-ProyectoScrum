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
  echo "Username: $username"
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
crearUsuario 'arturojara1999@fpuna.edu.py' 'Arturo' 'Jara' 'Arturo' 'None' 'Arturo'
crearUsuario 'alejandroadorno00@fpuna.edu.py' 'Alejandro' 'Adorno Quevedo' 'Alejandro' 'None' 'Ale'
crearUsuario 'jessicala182@gmail.com' 'Jessica' 'Alarcon' 'jessica' 'None' 'Jessi'
crearUsuario 'guillepaivag@gmail.com' 'Guillermo' 'Paiva' 'guillermo' 'None' 'Guille'
crearUsuario 'arturojeich@gmail.com' 'Arturo' 'Jara' 'arturo' 'None' 'Arturo'
crearUsuario 'arturojara1999@gmail.com' 'Arturo Gabriel' 'Jara Eichenbrenner' 'arturo' 'None' 'Arturo'

echo "Finalizando Script..."