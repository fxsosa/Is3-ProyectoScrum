##############################################
#                                            #
# Genera los index de docs sphinx, y abre    #
# la documentacion en el navegador por       #
# defecto.                                   #
#                                            #
##############################################

# Accediento al directorio
cd './documentacion'

sphinx-apidoc -o . ..

# Generando archivo html
make html

# Abriendo en el navegador por defecto
xdg-open "_build/html/index.html"
