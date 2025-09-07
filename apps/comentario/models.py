from django.db import models
from django.contrib.auth.models import User
from apps.post.models import Post

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f"Comentario de {self.autor.username} en post {self.post.pk}"
