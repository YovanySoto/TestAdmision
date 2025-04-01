from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    tipos = (
        ('cliente', 'Cliente'),
        ('operario', 'Operario')
    )
    # direccion = models.CharField(max_length=255, blank=False)
    # telefono = models.CharField(max_length=20, null=True)
    tipo = models.CharField(max_length=50, default='cliente', choices=tipos)
    user = models.OneToOneField(
        User, 
        related_name='userprofile', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        nombre = self.user.first_name
        apellido = self.user.last_name
        usuario = self.user.username
        tipo = self.tipo
        return f'{nombre} {apellido} | {usuario} | {tipo}'
