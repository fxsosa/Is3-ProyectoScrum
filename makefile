###########################################
# Para la documentacion #
###########################################
# 1. Inicializar/reinicializar
init-documentacion:
	bash './scripts/initDocumentacion.sh'
# 2. Abrir (en navegador predeterminado)
abrir-documentacion:
	bash './scripts/abrirDocumentacion.sh'

run-tests:
	pytest

generar-usuarios:
	bash './scripts/usuariosDePrueba.sh'

borrar-usuarios:
	bash './scripts/borrarUsuariosPrueba.sh'

limpiar-main:
	bash './scripts/clean_main.sh'