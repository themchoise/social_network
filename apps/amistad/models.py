from django.db import models
from django.contrib.auth.models import User

class Amistad(models.Model):
    ESTADOS = [
        ('pendiente', 'Solicitud Pendiente'),
        ('aceptada', 'Amistad Aceptada'),
        ('rechazada', 'Solicitud Rechazada'),
        ('bloqueada', 'Usuario Bloqueado'),
    ]
    
    usuario_solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    usuario_receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('usuario_solicitante', 'usuario_receptor')
        verbose_name = "Amistad"
        verbose_name_plural = "Amistades"
    
    def __str__(self):
        return f"{self.usuario_solicitante.username} -> {self.usuario_receptor.username}"

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
