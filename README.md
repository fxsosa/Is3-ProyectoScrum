# Sistema de Gestión de Proyectos
## Ingenieria de Software III
Pasos para levantar:
1. Levantar el contenedor
    ```
    docker-compose up
    ```
2. Abrir una terminal del contenedor
3. Levantar el servicio de postgresql
    ```
    /etc/init.d/postgresql start
    ```
4. Correr el makefile
    ```
    cd /usr/src/app/deploy_final
    ./deploy.sh dev
    ```
5. Ingresar 6 luego "y", luego enter hasta que salga "Password:" ahi ingresamos "admin" y luego que salgan letras rojas advirtiendo sobre la migracion, ahi debemos esperar a que termine el proceso de 
6. Enter
7. Enter
8. Enter

5. Darle enter hasta que salgan las letras rojas, ahi hay que esperar que las migraciones finalizen, se puede verificar de la siguiente manera:
    ```
    cat /usr/src/app/deploy_final/outputMigraciones.log
    ```
6. Una vez finalizado, ya se puede continuar dandole enter
## Ingeniería de Software II

## Descripción

Implementacion de un sistema de gestión de proyectos ágiles, 
facilitando el desarrollo de proyectos mediante la 
metodología SCRUM

## Acerca de
### Documentacion
- Para generar la documentacion
     ```
    make init-documentacion
    ```

- Para visualizar la documentacion
    ```
    make abrir-documentacion
    ```
### Deploy
- Deploy en el entorno de desarrollo
    ```
    make deploy-desarrollo
    ```
- Deploy en el entorno de producción
    ```
    make deploy-produccion
    ```



### Testeo
- Para testear el proyecto
    ```
    make run-tests
    ```

### Usuarios de Prueba
- Generar usuarios de prueba
    ```
    make generar-usuarios
    ```

- Borrar usuarios de prueba
    ```
    make borrar-usuarios
    ```

### Limpiar rep

- Limpiar la rama main (produccion) de archivos de basura
  ```
  make limpiar-main
  ```