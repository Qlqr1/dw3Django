from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alunos.views import (
    EstudanteViewSet,
    CursoViewSet,
    MatriculaViewSet,
    ListaMatriculasEstudante,
    ListaMatriculasCurso,
)

# O Router gera automaticamente todas as URLs do ViewSet
router = DefaultRouter()
router.register('estudantes', EstudanteViewSet, basename='estudantes')
router.register('cursos', CursoViewSet, basename='cursos')
router.register('matriculas', MatriculaViewSet, basename='matriculas')

urlpatterns = [
    path('', include(router.urls)),

    # Rotas manuais para os endpoints especiais
    path('estudantes/<int:pk>/matriculas/', ListaMatriculasEstudante.as_view()),
    path('cursos/<int:pk>/matriculas/', ListaMatriculasCurso.as_view()),
]