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
#   -> $7 : Is superuser True/False
crearUsuario(){
  email=$1
  nombres=$2
  apellidos=$3
  contrasenha=$4
  rol=$5
  username=$6
  is_superuser=$7
  echo ""
  echo "---------------------------------"
  echo "Usuario a registrar:"
  echo "Email: $email"
  echo "Nombres: $nombres"
  echo "Apellidos: $apellidos"
  echo "Contraseña: $contrasenha"
  echo "Rol: $rol"
  echo "Username: $username"
  echo "Es superuser: $is_superuser"
# Abrimos el shell de python
python3 manage.py shell<<-CONFIG
	from django.contrib.auth import get_user_model
	UserMan=get_user_model()
	user=UserMan.objects.create_user("$email", password="$contrasenha", nombres="$nombres", apellidos="$apellidos", rol=$rol, username="$username")
	user.is_superuser=$is_superuser
	user.save()
	exit()
	CONFIG
	echo "---------------------------------"
}

echo "Iniciando Script..."

# Creamos usuarios
crearUsuario 'arturojara1999@fpuna.edu.py' 'Arturo' 'Jara' 'Arturo' 'None' 'Arturo' 'False'
crearUsuario 'alejandroadorno00@fpuna.edu.py' 'Alejandro' 'Adorno Quevedo' 'Alejandro' 'None' 'Ale' 'False'
crearUsuario 'jessicala182@gmail.com' 'Jessica' 'Alarcon' 'jessica' 'None' 'Jessi' 'True'
crearUsuario 'guillepaivag@gmail.com' 'Guillermo' 'Paiva' 'guillermo' 'None' 'Guille' 'False'
crearUsuario 'arturojeich@gmail.com' 'Arturo' 'Jara' 'arturo' 'None' 'Arturo' 'False'
crearUsuario 'arturojara1999@gmail.com' 'Arturo Gabriel' 'Jara Eichenbrenner' 'arturo' 'None' 'Arturo' 'False'

echo "Finalizando Script..."