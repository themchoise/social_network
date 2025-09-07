from django.db import models
from django.contrib.auth.models import User
from apps.post.models import Post

# TODO: Modelo de Comentario
class Comentario(models.Model):
    # Relaciones
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    
    # TODO: Agregar campos del comentario
    # contenido = models.TextField(max_length=300)
    
    # Campos de fecha
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # TODO: Agregar campos adicionales
    # activo = models.BooleanField(default=True)
    # likes_count = models.PositiveIntegerField(default=0)
    
    # TODO: Para comentarios anidados (respuestas)
    # comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, 
    #                                    blank=True, null=True, related_name='respuestas')
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['fecha_creacion']  # Más antiguos primero
    
    def __str__(self):
        # TODO: Personalizar representación
        return f"Comentario de {self.autor.username} en post {self.post.pk}"
        # return f"{self.autor.username}: {self.contenido[:30]}..."
    
    # TODO: Método para verificar si es una respuesta
    # def es_respuesta(self):
    #     return self.comentario_padre is not None
