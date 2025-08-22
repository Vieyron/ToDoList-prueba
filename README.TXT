API REST desarrollada con Django y Django REST Framework para gestionar tareas con autenticación básica.

# Requisitos Previos

## Software necesario:
- Abrir con visual studio code
- Python 3.8 o superior
- pip 

## Instalación de dependencias:
``` en terminal de visual  studio(que fue mi caso) ó en cmd
pip install django djangorestframework

## Aplicar migraciones
(Hay una tarea que no tiene ID pero aún así esta creada, para poder borrarla solo se tiene que borrar el archivo ToDoList.db
y hacer los comandos que siguen)
``` en terminal de visual  studio
python manage.py migrate

## Crear usario administrador
``` en terminal de visual  studio
python manage.py createsuperuser

``Esto para el super Usuario(admin)
- Usuario: user
- Contraseña: 123456
- Email: (opcional, puede dejarse en blanco)
- si dice que la contraseña es muy corta o muy sencilla de igual dar acceso para la prueba dando en la tecla "y"

## Iniciar servidor de forma local
``` en terminal de visual  studio
python manage.py runserver

## Credenciales de API
Autenticación Basic Auth:
`` Esto lo va a pedir solo cuando se necesite hacer una busqueda de una tarea y posiblemente solo lo va a pedir una vez, esto porque se queda
guardada en el navegador, pero cuando se cierre el navegador por completo y se vuelva abrir, la va a pedir de nuevo 
Usuario: admin
Contraseña: password123
``Esta se pone en el cmd con los curls
Header: Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=

Pruebas de la API con CURL
``` esto en CMD

1. Crear una tarea (POST):
curl -X POST http://127.0.0.1:8000/tasks/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d "{\"codigo\": \"TEST01\", \"nombre\": \"Mi tarea\", \"descripcion\": \"Descripción\"}"

2. Listar todas las tareas (GET):
curl -X GET http://127.0.0.1:8000/tasks/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

3. Obtener tarea específica (GET):
curl -X GET http://127.0.0.1:8000/tasks/TEST01/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

4. Actualizar tarea (PUT):
curl -X PUT http://127.0.0.1:8000/tasks/TEST01/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d "{\"nombre\": \"Nombre actualizado\"}"

5. Eliminar tarea (DELETE):
curl -X DELETE http://127.0.0.1:8000/tasks/TEST01/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

## Pruebas de Manejo de Errores
``` esto en CMD
Error 401 - Sin autenticación:
curl -X GET http://127.0.0.1:8000/tasks/

Error 401 - Credenciales incorrectas:
curl -X GET http://127.0.0.1:8000/tasks/ -H "Authorization: Basic wrongcredentials"

Error 404 - Tarea no encontrada:
curl -X GET http://127.0.0.1:8000/tasks/NOEXISTE/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

Error 400 - Datos inválidos:
curl -X POST http://127.0.0.1:8000/tasks/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d "{\"codigo\": \"ABC\"}"

para este se debe de ingresar en la carpeta de aplicacions/api y entrar en views.py, despues debe descomentar la linea 79, para tener el error en el servidor, recuerde
volver a comentar para que sirva 
Error 500 - Error interno (forzado):
curl -X POST http://127.0.0.1:8000/tasks/ -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d "JSON_INVALIDO"


