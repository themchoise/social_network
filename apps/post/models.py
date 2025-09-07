from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Post de {self.autor.username} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('post:detalle', kwargs={'pk': self.pk})

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'post')
        verbose_name = "Me Gusta"
        verbose_name_plural = "Me Gusta"
    
    def __str__(self):
        return f"{self.usuario.username} le gusta el post {self.post.pk}"
