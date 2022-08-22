##############################################
#                                            #
# Genera los index de docs sphinx, y abre    #
# la documentacion en el navegador por       #
# defecto.                                   #
#                                            #
##############################################

# Actualizamos el index
cd "./documentacion"

# Actualizamos el index.rst con los modulos del proyecto
sed -i 's/:caption: Contents:/&\n   usuarios/' './index.rst'
sed -i 's/:caption: Contents:/&\n   tests/' './index.rst'
sed -i 's/:caption: Contents:/&\n   settings/' './index.rst'
sed -i 's/:caption: Contents:/&\n   roles/' './index.rst'
sed -i 's/:caption: Contents:/&\n   ProyectoScrum/' './index.rst'
sed -i 's/:caption: Contents:/&\n   app/' './index.rst'
sed -i 's/:caption: Contents:/&\n/' './index.rst'

sphinx-apidoc -o . ..

# Generando archivo html
make html

# Abriendo en el navegador por defecto
xdg-open "_build/html/index.html"
