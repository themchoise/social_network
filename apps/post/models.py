from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# TODO: Modelo de Publicación
class Post(models.Model):
    # Relación con el usuario que crea el post
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # TODO: Agregar campos del post
    # contenido = models.TextField(max_length=500)
    # imagen = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    # Campos de fecha y estado
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # TODO: Agregar campos de interacción
    # activo = models.BooleanField(default=True)
    # likes_count = models.PositiveIntegerField(default=0)
    # comentarios_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['-fecha_creacion']  # Más recientes primero
    
    def __str__(self):
        # TODO: Personalizar la representación
        return f"Post de {self.autor.username} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
        # return f"{self.autor.username}: {self.contenido[:50]}..."
    
    # TODO: Método para obtener URL del post
    def get_absolute_url(self):
        return reverse('post:detalle', kwargs={'pk': self.pk})

# TODO: Modelo de Like
class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'post')  # Un usuario solo puede dar un like por post
        verbose_name = "Me Gusta"
        verbose_name_plural = "Me Gusta"
    
    def __str__(self):
        return f"{self.usuario.username} le gusta el post {self.post.pk}"
