#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork_project.settings')
django.setup()

from apps.user.models import User

# Verificar usuario existente
user = User.objects.first()
if user:
    print(f"✓ Usuario encontrado: {user.username} ({user.email})")
else:
    print("✗ No hay usuarios en la base de datos")
    
# Listar usuarios
print(f"\nTotal de usuarios: {User.objects.count()}")
for u in User.objects.all()[:5]:
    print(f"  - {u.username}: {u.email}")
