from django.db import models

# ──────────────────────────────────────────────
# O que é um Model?
# É uma classe Python que representa uma tabela no banco.
# Cada atributo da classe = uma coluna na tabela.
# ──────────────────────────────────────────────

class Estudante(models.Model):
    # CharField = texto de tamanho limitado
    nome = models.CharField(max_length=100)

    # EmailField = como CharField, mas valida formato de email
    email = models.EmailField(unique=True)  # unique=True impede emails repetidos

    # CPF como texto para preservar zeros à esquerda (ex: 012.345.678-99)
    cpf = models.CharField(max_length=14, unique=True)

    # DateField = armazena só a data (sem hora)
    data_nascimento = models.DateField()

    def __str__(self):
        # Esse método define o que aparece quando você imprime o objeto
        return self.nome


class Curso(models.Model):
    # Choices = lista de opções válidas para o campo "nivel"
    NIVEL_CHOICES = [
        ('B', 'Básico'),
        ('I', 'Intermediário'),
        ('A', 'Avançado'),
    ]

    codigo = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=100)
    nivel = models.CharField(
        max_length=1,
        choices=NIVEL_CHOICES,
        default='B'
    )

    def __str__(self):
        return self.descricao


class Matricula(models.Model):
    PERIODO_CHOICES = [
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
        ('N', 'Noturno'),
    ]

    # ForeignKey = chave estrangeira (ligação entre tabelas)
    # on_delete=CASCADE: se o estudante for deletado, a matrícula também é
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name='matriculas'  # permite acessar estudante.matriculas.all()
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='matriculas'
    )
    periodo = models.CharField(max_length=1, choices=PERIODO_CHOICES)

    def __str__(self):
        return f'{self.estudante} → {self.curso}'