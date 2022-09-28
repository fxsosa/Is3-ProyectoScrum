from django.db import models
import datetime

from usuarios.models import Usuario
from django.apps import apps

class ManejoProyectos(models.Manager):
    """
    Manager del modelo de Proyectos
    """

    def importarRoles(self, datos):
        """Metodo para la importacion de roles de usuario asociados a un proyecto, a otro proyecto

        :param datos: Datos de request con el siguiente formato:
            {"idProyectoActual": "id1", "idProyectoExterno": "id2"}
            El primer id referencia al proyecto a recibir los roles, el segundo, al proyecto del cual importar sus roles

        :return: Lista de Roles agregados
        """



        idProyectoActual = datos['idProyectoActual']
        idProyectoExterno = datos['idProyectoExterno']

        # Se valida en los controllers
        proyectoActual = Proyecto.objects.get(id=idProyectoActual)
        proyectoExterno = Proyecto.objects.get(id=idProyectoExterno)
        listaRoles = apps.get_model('roles.Rol').objects.filter(proyecto=idProyectoExterno)
        listaRolesActuales = apps.get_model('roles.Rol').objects.filter(proyecto=idProyectoActual)
        listaNuevosRoles = []

        for r in listaRoles:
                rolNuevo = apps.get_model('roles.Rol').objects.crearRolInterno(nombre=r.nombre, descripcion=r.descripcion, idProyecto=proyectoActual.id)
                listaPermisosExterno = apps.get_model('roles.Rol').objects.listarPermisos(id=r.id)
                listaPermisosActual = []
                for perm in listaPermisosExterno:
                    listaPermisosActual.append({"nombre": "proyectos." + perm.codename, "idObjeto": idProyectoActual})

                # Agregamos permisos de objeto
                apps.get_model('roles.Rol').objects.agregarListaPermisoObjeto(r=rolNuevo, lista=listaPermisosActual)
                listaNuevosRoles.append(rolNuevo)

        return listaNuevosRoles


    def crearProyecto(self, datos):
        """Metodo para la creacion de proyectos.

        :param datos: Datos de un request.data con el siguiente formato
            {"nombre": String, "descripcion": String, "fechaInicio": DATE, "fechaFin": DATE, "scrumMaster": email, "estado": String}

        :return: None
        """

        nombre = datos['nombre']
        descripcion = datos['descripcion']
        fechaInicio = datos['fechaInicio']
        fechaFin = datos['fechaFin']
        scrumMaster = Usuario.objects.get(email=datos['scrumMaster']) # Obtenemos el usuario Scrum Master por su id, que es su correo
        estado = "planificación"
        proyecto = self.model(nombre=nombre, descripcion=descripcion, fechaInicio=fechaInicio,
                              fechaFin=fechaFin, scrumMaster=scrumMaster, estado=estado)
        proyecto.save()


        return proyecto
    #TODO: Añadir fecha de fin automáticamente cuando el SM finalice el proyecto

    def modificarProyecto(self, datos):
        """Metodo para la actualizacion de los parametros de un proyecto

        :param datos: Diccionario recibido de un request.data
                Contiene nombre y descripcion

        :return: Instancia Proyecto
        """
        proyecto = Proyecto.objects.get(id=int(datos['id']))
        proyecto.nombre = datos['nombre']
        proyecto.descripcion = datos['descripcion']
        # El estado del proyecto no se modifica manualmente, sino automáticamente

        proyecto.save()
        return proyecto

    def iniciarProyecto(self, datos):
        """Metodo para cambiar el estado de proyecto a Iniciado
        
        :param datos: Diccionario recibido como request.data
        Contiene "estado" String, y "fechaInicio" DATE
        
        :return: Instancia de Proyecto actualizado
        """
        proyecto = Proyecto.objects.get(id=int(datos['id']))
        proyecto.estado = "iniciado"
        proyecto.fechaInicio = datetime.date.today()
        proyecto.save()
        return proyecto

class ManejoParticipantes(models.Manager):
    """
    Manager del modelo de Participantes de proyecto
    """


    def crearParticipante(self, datos):
        """Metodo para crear un participante y asignarlo a un proyecto ya inicializado

        :param datos: Diccionario recibido de un request.data
        Contiene "idProyecto" Integer, y "idUsuario" Integer.

        :return: Instancia de Participante
        """
        proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
        usuario = Usuario.objects.get(id=int(datos['idUsuario']))

        if self.filter(proyecto=proyecto, usuario=usuario).exists():
            return None

        participante = self.model(proyecto=proyecto, usuario=usuario)

        participante.save()

        return participante

    def listarProyectosdeParticipante(self, id):
        """Metodo para listar los IDs de los proyectos en los que participa un usuario

        :param id: Id del usuario/participante

        :return: Lista de Int (IDs de los proyectos)
        """

        listaQuery = participante.objects.filter(usuario_id=id).values("proyecto")

        print("listaQuery = ", listaQuery)
        proyectos = []
        for i in range(len(listaQuery)):
            idProyecto = listaQuery[i]['proyecto']
            proyectos.append(Proyecto.objects.get(id=int(idProyecto)))

        print("proyectosID", proyectos)

        return proyectos

    def listarParticipantedeProyectos(self, idProyecto):
        """Metodo para listar a los participantes de un proyecto

        :param idProyecto: ID del proyecto

        :return: Lista (Usuario)
        """

        listaQuery = participante.objects.filter(proyecto=idProyecto).values("usuario")

        print("listaQuery = ", listaQuery)
        usuarios = []
        for i in range(len(listaQuery)):
            idUsuario = listaQuery[i]['usuario']
            usuarioAgg = Usuario.objects.get(id=int(idUsuario))
            usuarios.append(usuarioAgg)

        print("usuarios", usuarios)

        return usuarios

    def borrarParticipante(self, user,proyecto):
        """Metodo para eliminar participante de un proyecto

        :param user: Instancia Usuario
        :param proyecto: Instancia Proyecto

        :return: None
        """
        particip = participante.objects.get(usuario=user, proyecto=proyecto)
        particip.delete()



    # Falta corregir este método para el put, no funciona
    '''
    def modificarParticipante(self, datos):
        particip = participante.objects.get(id=int(datos['idParticipante']))
        particip.proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
        #particip.usuario = Usuario.objects.get(id=int(datos['idUsuario'])) # Busca con id
        particip.usuario = Usuario.objects.get(email=datos['mailUsuario'])
        # El estado del proyecto no se modifica manualmente, sino automáticamente

        proyecto.save()
        return proyecto
    '''



class Proyecto(models.Model):
    """
        Clase de Proyectos
    """

    #El id se genera de forma automática
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateTimeField(null=True) #Incluye minutos y segundos
    fechaFin = models.DateTimeField(null=True)
    scrumMaster = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True) #Evita que se borre, se soluciona cambiando de Scrum Master y luego borrando al usuario
    estado = models.CharField(max_length=30)

    objects = ManejoProyectos()
    def __str__(self):
        return str([self.nombre, self.descripcion, self.fechaInicio, self.fechaFin,
                    self.scrumMaster.id, self.estado])

    class Meta:
        """
            Clase con los permisos del modelo de proyectos
        """
        #default_permissions = ()  # ?deshabilitamos add/change/delete/view

        permissions = (
            ('crear_proyecto', 'Crear un nuevo proyecto'),
            ('eliminar_proyecto', 'Eliminar un proyecto'),
            ('actualizar_proyecto', 'Actualizar los parametros iniciales de un proyecto'),
            ('archivar_proyecto', 'Archivar un proyecto'),
            ('cambiar_estado_proyecto', 'Modificar el estado de un proyecto'),
            ('listar_proyectos', 'Listar uno o varios proyectos'),
            ('iniciar_proyecto', 'Marcar un proyecto como iniciado'),
            ('crear_tipo_HU', 'Crear un nuevo tipo de Historia de Usuario'),
            ('borrar_tipo_HU', 'Borrar un tipo de HU'),
            ('importar_tipo_HU', 'Importar un tipo de HU'),
            ('importar_roles_internos', 'Importar roles internos de otro proyecto'),
            ('agregar_participante', 'Agregar un usuario a un proyecto'),
            ('modificar_participante', 'Modificar un participante'),
            ('borrar_participante', 'Borrar participante'),
            ('listar_participante', 'Lista un participante individual'),
            ('listar_roles_internos', 'Listar todos los roles internos del sistema'),
            ('crear_rol_interno', 'Crear un nuevo rol interno'),
            ('actualizar_rol_interno', 'Actualizar un rol interno'),
            ('borrar_rol_interno', 'Borrar un rol interno de proyecto'),
            ('modificar_columnas_tipo_HU', 'Añadir, eliminar o modificar columnas de un tipo de HU'),
            ('actualizar_tipo_HU', 'Actualizar un tipo de Historia de Usuario'),
            ('listar_historias_usuario', 'Listar las historias de usuario de un proyecto'),
            ('obtener_historia_usuario', 'Obtener una historia de usuario de un proyecto'),
            ('crear_historia_usuario', 'Crear y agregar una historia de usuario a un proyecto'),
            ('actualizar_historia_usuario', 'Actualizar una historia de usuario de un proyecto'),
            ('borrar_historia_usuario', 'Borrar una historia de usuario de un proyecto'),
            ('listar_sprint_proyecto', 'Listar los sprints de un proyecto'),
            ('crear_sprint', 'Crear y agregar un sprint a un proyecto'),
            ('obtener_sprint', 'Obtiene un sprint de un proyecto'),
            ('borrar_sprint', 'Borrar un sprint de un proyecto'),
        )
# Participante de un proyecto (separado de usuario)
class participante(models.Model):
    """
        Clase para el modelo de participantes
    """
    # El id se genera de modo automático
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE) # Se elimina el proyecto, se eliminan sus participantes
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # Si borramos el usuario, se borran todas sus participaciones
    objects=ManejoParticipantes()
    def __str__(self):
        return str([self.proyecto, self.usuario])
