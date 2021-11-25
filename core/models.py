from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Escola(models.Model):
    id_escola = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'Escola'


class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    t_ano = models.IntegerField(null=True, blank=True)
    t_turma = models.CharField(max_length=20, null=True, blank=True)
    t_escola = models.ForeignKey('Escola', on_delete=models.CASCADE, to_field='id_escola')

    class Meta:
        db_table = 'Turma'

    def __str__(self):
        return self.t_turma


class Aula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    au_turma = models.ForeignKey('Turma', on_delete=models.CASCADE, to_field='id_turma')
    au_disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE, to_field='id')

    class Meta:
        db_table = 'Aula'


class Aluno(models.Model):
    id_aluno = models.IntegerField(primary_key=True)
    al_nome = models.CharField(max_length=120, unique=True)
    al_chamada = models.IntegerField(null=True)
    al_disciplina = models.ManyToManyField('Disciplina', blank=True)
    al_turma = models.ForeignKey('Turma', on_delete=models.CASCADE, null=True, blank=True)

    al_usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # atributo da aplicação
    al_grupo = models.ForeignKey(Group, on_delete=models.CASCADE)  # atributo da aplicação

    class Meta:
        db_table = 'Aluno'

    def __str__(self):
        return self.al_nome


class Presenca(models.Model):
    id_aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
    id_presenca = models.BooleanField(default=False)
    id_aluno = models.ManyToManyField('Aluno')
    data_aula = models.DateTimeField(auto_now=True)
    qte_aulas = models.IntegerField(default=25, null=True, blank=True)

    class Meta:
        db_table = 'Presenca'


class Disciplina(models.Model):
    d_nome = models.CharField(max_length=40, unique=True)
    d_professor = models.ForeignKey('Professor', on_delete=models.CASCADE, to_field='id', null=True, blank=True)

    class Meta:
        db_table = 'Disciplina'

    def __str__(self):
        return self.d_nome


class Professor(models.Model):
    p_nome = models.CharField(max_length=120, unique=True)
    p_disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE, to_field='id', null=True, blank=True)
    p_usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    p_grupo = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Professor'

    def __str__(self):
        return self.p_nome
