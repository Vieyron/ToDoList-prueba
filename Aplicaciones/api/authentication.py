from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

class BasicAuthCustom(authentication.BasicAuthentication):
    """
    Autenticación básica personalizada que valida contra credenciales predefinidas
    """
    def authenticate_credentials(self, userid, password, request=None):
        
        if userid in settings.BASIC_AUTH_CREDENTIALS:
            if password == settings.BASIC_AUTH_CREDENTIALS[userid]:
                # Obtener o crear un usuario de Django válido
                user, created = User.objects.get_or_create(
                    username=userid,
                    defaults={
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True
                    }
                )
                
                return (user, None)
        
        # Si las credenciales no coinciden, lanzar excepción
        raise exceptions.AuthenticationFailed('Invalid username/password.')