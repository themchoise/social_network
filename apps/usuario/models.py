from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class PerfilUsuario(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre = models.TextField(max_length=100, blank=True)
    
    # Relación con Carrera
    carrera = models.ForeignKey('Carrera', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

   
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    def get_absolute_url(self):
        return reverse('usuario:perfil', kwargs={'username': self.usuario.username})

class Carrera(models.Model):
    nombre = models.CharField(max_length=200)
    acronmico = models.CharField(max_length=10) 
   
    def __str__(self):
        return {
            'nombre': self.nombre,
            'acronmico': self.acronmico
        }

