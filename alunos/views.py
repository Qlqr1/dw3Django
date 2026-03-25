from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from alunos.throttles import MatriculaRateThrottle
from alunos.models import Estudante, Curso, Matricula
from alunos.serializers import (
    EstudanteSerializer,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,
    ListaMatriculasCursoSerializer,
)


# ──────────────────────────────────────────────
# ModelViewSet gera automaticamente 5 rotas:
#   GET    /estudantes/        → lista todos
#   POST   /estudantes/        → cria novo
#   GET    /estudantes/{id}/   → busca um
#   PUT    /estudantes/{id}/   → atualiza um
#   DELETE /estudantes/{id}/   → deleta um
# ──────────────────────────────────────────────

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
    # Campos que podem ser usados para busca (?search=joao)
    search_fields = ['nome', 'cpf']
    # Campos que podem ser usados para ordenação (?ordering=nome)
    ordering_fields = ['nome']
    # Campos que podem ser filtrados exatamente (?nome=Joao)
    filterset_fields = ['ativo']  # exemplo: filtrar estudantes ativos
    # Somente administradores podem criar/editar/deletar estudantes
    permission_classes = [IsAdminUser]


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    search_fields = ['codigo', 'descricao']
    ordering_fields = ['descricao']
    filterset_fields = ['nivel']  # filtrar por nível: ?nivel=B
    # Qualquer usuário autenticado pode ver e editar cursos
    permission_classes = [IsAuthenticated]


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    ordering_fields = ['periodo']
    filterset_fields = ['periodo']  # filtrar por período: ?periodo=M
    permission_classes = [IsAuthenticated]
    throttle_classes = [MatriculaRateThrottle]


# ──────────────────────────────────────────────
# ListAPIView: somente leitura (GET), sem criar/editar/deletar
# Usamos para as rotas especiais de matrículas por estudante e por curso
# ──────────────────────────────────────────────

class ListaMatriculasEstudante(generics.ListAPIView):
    # Aqui filtramos as matrículas pelo ID do estudante que vem na URL
    def get_queryset(self):
        # self.kwargs['pk'] pega o {pk} da URL
        return Matricula.objects.filter(estudante_id=self.kwargs['pk'])

    serializer_class = ListaMatriculasEstudanteSerializer
    permission_classes = [IsAuthenticated]


class ListaMatriculasCurso(generics.ListAPIView):
    def get_queryset(self):
        return Matricula.objects.filter(curso_id=self.kwargs['pk'])

    serializer_class = ListaMatriculasCursoSerializer
    permission_classes = [IsAuthenticated]