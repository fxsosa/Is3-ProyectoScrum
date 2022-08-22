##############################################
#                                            #
# Script para la borrar los usuarios de      #
# prueba generados a nivel local             #
#                                            #
##############################################

echo "Iniciando script..."
# Eliminando registros
python3 manage.py shell<<-CONFIG
	from django.contrib.auth import get_user_model
	UserMan=get_user_model()
	UserMan.objects.all().delete()
	exit()
	CONFIG

echo "Finalizando script..."
