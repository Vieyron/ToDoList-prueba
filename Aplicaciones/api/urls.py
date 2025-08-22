from django.urls import path
from . import views

urlpatterns = [
    # endpoints API REST con autenticación
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='api_tasks_list'),
    path('tasks/<str:codigo>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='api_tasks_detail'),
    path('tasks/search/', views.task_search, name='api_tasks_search'),
    
    # URLs web 
    path('', views.home, name='home'),
    path('registrarTarea/', views.registrar_tarea, name='registrar_tarea'),
    path('eliminarTarea/<str:codigo>/', views.eliminar_tarea, name='eliminar_tarea'),
    
    path('api/tareas/', views.TaskListCreateAPIView.as_view(), name='api_tareas_list'),
    path('api/tareas/<str:codigo>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='api_tareas_detail'),
]