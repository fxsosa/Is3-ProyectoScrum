# Sistema de Gestión de Proyectos
## Ingenieria de Software III
Pasos para levantar por primera vez:
1. Levantar el contenedor
    ```
    docker-compose up
    ```
2. Abrir una terminal del contenedor(attach terminal)
3. Correr el deploy.sh
    ```
    cd /usr/src/app/deploy_final/
    source /usr/src/app/deploy_final/deploy.sh dev
    ```
5. Ingresar 6 luego "y", luego enter hasta que salga "Password:" ahi ingresamos "admin" y luego hasta que salgan las letras rojas advirtiendo sobre la migracion, ahi debemos esperar a que termine el proceso de migracion, se imprime en el log de outputMigracion.log
6. Una vez finalizado, ya se puede continuar dandole enter
7. El proyecto deberia de estar levantado en: localhost:8080

Pasos para levantar luego de la primera vez:
1. Abrir el venv del backend y luego levantarlo
    ```
    source /usr/src/app/deploy_final/ProyectoScrum/venv/bin/activate
    cd /usr/src/app/ProyectoScrum
    python3 manage.py runserver
    ```
2. Levantar el front
    ```
    cd /usr/src/app/deploy_final/ProyectoScrumFrontend
    npm run serve
    ```
3. El proyecto deberia de estar levantado en: localhost:8080
    

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