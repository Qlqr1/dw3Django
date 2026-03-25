from rest_framework import serializers
from alunos.models import Estudante, Curso, Matricula
from validate_docbr import CPF  # pip install validate-docbr


# ──────────────────────────────────────────────
# ModelSerializer: gera automaticamente os campos
# a partir do model. Você só precisa dizer qual
# model usar e quais campos incluir.
# ──────────────────────────────────────────────

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante        # qual model usar
        fields = '__all__'       # incluir todos os campos

    def validate_cpf(self, value):
        # Esse método é chamado automaticamente pelo DRF ao validar o campo "cpf"
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("CPF inválido.")
        return value

    def validate_nome(self, value):
        # Verifica se o nome tem pelo menos dois caracteres e só letras/espaços
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("O nome deve conter apenas letras.")
        return value


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


# Serializer padrão da Matricula (mostra os IDs)
class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'


# ──────────────────────────────────────────────
# Serializer "detalhado": mostra o nome do estudante
# e do curso em vez de só o ID numérico.
# Útil para leitura (GET), mais legível.
# ──────────────────────────────────────────────
class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    # SerializerMethodField: campo calculado (não vem direto do model)
    curso_nome = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ['id', 'curso_nome', 'periodo']

    # O método precisa se chamar get_<nome_do_campo>
    def get_curso_nome(self, obj):
        return obj.curso.descricao


class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ['id', 'estudante_nome', 'periodo']

    def get_estudante_nome(self, obj):
        return obj.estudante.nome