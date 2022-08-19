from django.db import models
from usuarios.models import Usuario


class Sprint(models.Model):
    """
    Representación del modelo de Sprint

    ...
    Attributes
    ----------
    fecha_inicio : DateField
        la fecha y hora prevista para el inicio del Sprint.
    fecha_fin : DateTime
        la fecha y hora prevista para el final del Sprint.
    capacidadEquipo : Integer
        capacidad, en horas, de trabajo asumible por el equipo del Sprint.
    estado : Str
        Creado, En Espera, En Ejecucion, Culminado, Cancelado
    """

    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)
    capacidadEquipo = models.IntegerField(null=False)
    estado = models.TextField(max_length=10)

    def __str__(self):
        return str([self.fecha_inicio, self.fecha_fin, self.capacidadEquipo,
                    self.estado])


class SprintBacklog(models.Model):
    """
          Representación del modelo de backlog de Sprint

        ...
        Attributes
        ----------
        idHistoriaUsuario : Historia_Usuario
            Foreign key a una historia de usuario (la lista de historias
            es lo que forma el Backlog)
        idSprint : Sprint
            Foreign key del Sprint al cual está asociado este Backlog
    """


    # idHistoriaUsuario = models.ForeignKey(Historia_Usuario)
    idSprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str([self.idSprint.id, self.idHistoriaUsuario])


class SprintEquipo(models.Model):
    """
        Representación de la lista de usuarios de un Sprint dado.

        ...
        Attributes
        ----------
        usuario : HistoriaUsuario
            Foreign Key al usuario participante de este equipo
        sprint : Sprint
            Foreign Key referenciando el Sprint al cual este usuario
            pertenece.
        trabajo: CharField
            ??? ??? ???
        capacidad : IntegerField
            Capacidad (int en horas) del Usuario participante de este equipo
    """

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    trabajo = models.CharField(max_length=80)
    capacidad = models.IntegerField()

    def __str__(self):
        return str([self.usuario.id, self.sprint.id, self.trabajo,
                    self.capacidad.__str__()])

