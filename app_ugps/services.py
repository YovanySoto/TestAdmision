from django.contrib.auth.models import User
from .models import UserProfile
from django.db import IntegrityError

def crear_usuario(username: str, first_name: str, last_name: str, email: str, password: str) -> bool:
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            raise ValueError('El nombre de usuario ya existe')
            
        if User.objects.filter(email=email).exists():
            raise ValueError('El email ya está registrado')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Crear perfil
        UserProfile.objects.create(
            user=user,
            tipo='cliente'
        )
        
        return True
        
    except IntegrityError as e:
        print(f"Error de base de datos: {str(e)}")
        return False
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return False
    