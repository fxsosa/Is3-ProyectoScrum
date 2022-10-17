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

# Abriendo en el navegador disponible (firefox, chrome)
# xdg-open "_build/html/index.html"
temp1=$(firefox --version)
temp2=$('google-chrome' --version)

if [[ "$temp1" =~ "Mozilla Firefox " ]]; then
  firefox "_build/html/index.html"
elif [[ "$temp2" =~ "Google Chrome ".* ]]; then
  'google-chrome' "_build/html/index.html"
fi
