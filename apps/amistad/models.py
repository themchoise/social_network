from django.db import models
from django.contrib.auth.models import User

# TODO: Modelo de Amistad/Seguimiento
class Amistad(models.Model):
    # Opciones de estado de la amistad
    ESTADOS = [
        ('pendiente', 'Solicitud Pendiente'),
        ('aceptada', 'Amistad Aceptada'),
        ('rechazada', 'Solicitud Rechazada'),
        ('bloqueada', 'Usuario Bloqueado'),
    ]
    
    # Relaciones
    usuario_solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    usuario_receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    
    # TODO: Agregar campos de estado
    # estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    # Fechas
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('usuario_solicitante', 'usuario_receptor')
        verbose_name = "Amistad"
        verbose_name_plural = "Amistades"
    
    def __str__(self):
        return f"{self.usuario_solicitante.username} -> {self.usuario_receptor.username}"
    
    # TODO: Métodos útiles
    # def aceptar(self):
    #     self.estado = 'aceptada'
    #     self.fecha_respuesta = timezone.now()
    #     self.save()
    
    # def rechazar(self):
    #     self.estado = 'rechazada'
    #     self.fecha_respuesta = timezone.now()
    #     self.save()

# TODO: Modelo de Seguimiento (alternativa más simple a amistad)
class Seguimiento(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='siguiendo')
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    fecha_seguimiento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('seguidor', 'seguido')
        verbose_name = "Seguimiento"
        verbose_name_plural = "Seguimientos"
    
    def __str__(self):
        return f"{self.seguidor.username} sigue a {self.seguido.username}"
