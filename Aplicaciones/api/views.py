from rest_framework import generics, status, exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Tarea
from .serializers import TareaSerializer
from .authentication import BasicAuthCustom
import base64

# vistas API con autenticación básica
@authentication_classes([BasicAuthCustom])
@permission_classes([IsAuthenticated])
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tarea.objects.all().order_by('-creado')
    serializer_class = TareaSerializer

    def get_serializer_context(self):
        # Pasar el request al serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.ValidationError):
            return Response(
                {'error': 'Datos de entrada inválidos', 'details': exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, exceptions.AuthenticationFailed):
            response = HttpResponse('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
            response['WWW-Authenticate'] = 'Basic realm="API"'
            return response
        return super().handle_exception(exc)

@authentication_classes([BasicAuthCustom])
@permission_classes([IsAuthenticated])
class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    lookup_field = 'codigo'

    def get_serializer_context(self):
        # pasar el request al serializer para saber el método
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Tarea.DoesNotExist:
            return Response(
                {'error': 'Tarea no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.NotFound):
            return Response(
                {'error': 'Tarea no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        elif isinstance(exc, exceptions.AuthenticationFailed):
            response = HttpResponse('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
            response['WWW-Authenticate'] = 'Basic realm="API"'
            return response
        return super().handle_exception(exc)

# vista para búsqueda con autenticación
@api_view(['GET'])
@authentication_classes([BasicAuthCustom])
@permission_classes([IsAuthenticated])
def task_search(request):
    try:
        # Forzar error aquí
        #raise Exception("Error 500 de prueba intencional")
    
        query = request.GET.get('q', '')
        if query:
            tareas = Tarea.objects.filter(
                nombre__icontains=query
            ) | Tarea.objects.filter(
                descripcion__icontains=query
            )
        else:
            tareas = Tarea.objects.all()
        
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Error interno del servidor', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# middleware para manejar autenticación básica
class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # aplicar solo a endpoints API que requieren autenticación
        if request.path.startswith('/tasks/') or request.path.startswith('/api/tareas/'):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if not auth_header.startswith('Basic '):
                response = HttpResponse('Unauthorized', status=401)
                response['WWW-Authenticate'] = 'Basic realm="API"'
                return response
            
            try:
                auth_decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
                username, password = auth_decoded.split(':', 1)
                
                from django.conf import settings
                if username in settings.BASIC_AUTH_CREDENTIALS and password == settings.BASIC_AUTH_CREDENTIALS[username]:
                    # autenticación exitosa
                    return self.get_response(request)
                else:
                    response = HttpResponse('Unauthorized', status=401)
                    response['WWW-Authenticate'] = 'Basic realm="API"'
                    return response
            except:
                response = HttpResponse('Unauthorized', status=401)
                response['WWW-Authenticate'] = 'Basic realm="API"'
                return response
        
        return self.get_response(request)

# vistas para la interfaz web (sin autenticación)
def home(request):
    tareas_listadas = Tarea.objects.all().order_by('-creado')
    return render(request, "gestionTareas.html", {"tareas": tareas_listadas})

def registrar_tarea(request):
    if request.method == 'POST':
        codigo = request.POST.get('txtCodigo')
        nombre = request.POST.get('txtNombre')
        descripcion = request.POST.get('txtDescripcion')
        modo_edicion = request.POST.get('modoEdicion') == 'true'
        
        if codigo and nombre:
            try:
                if modo_edicion:
                    tarea = get_object_or_404(Tarea, codigo=codigo)
                    tarea.nombre = nombre
                    tarea.descripcion = descripcion or ''
                    tarea.save()
                    return redirect('/?success=1')
                else:
                    if Tarea.objects.filter(codigo=codigo).exists():
                        return redirect('/?error=1&message=Código ya existe')
                    Tarea.objects.create(
                        codigo=codigo,
                        nombre=nombre,
                        descripcion=descripcion or ''
                    )
                    return redirect('/?success=1')
            except Exception as e:
                return redirect(f'/?error=1&message={str(e)}')
    
    return redirect('/')

def eliminar_tarea(request, codigo):
    try:
        tarea = Tarea.objects.get(codigo=codigo)
        tarea.delete()
        return redirect('/?success=1')
    except Tarea.DoesNotExist:
        return redirect('/?error=1&message=Tarea no encontrada')
    except Exception as e:
        return redirect(f'/?error=1&message={str(e)}')
    