from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from core.models import *
import os

# Create your views here.

@login_required(login_url='login/')
def chamada(request):

    cont = 1
    if request.POST.get('cont'):  # iterador da turma
        if request.POST.get('desfazer') == 'desfazer':
            cont = int(request.POST.get('cont')) - 1
        else:
            cont = int(request.POST.get('cont')) + 1

    try:
        t_teste = Turma.objects.get(t_turma=request.POST.get('turma'))
        d_teste = Disciplina.objects.get(d_nome=request.POST.get('disciplina'))
    except:
        return redirect('/not-found')

    alunos_turma = {}

    # Iniciando a aula
    turma = request.POST.get('turma')
    au_turma = Turma.objects.get(t_turma=turma)

    disciplina = request.POST.get('disciplina')
    au_disciplina = Disciplina.objects.get(d_nome=disciplina)

    aula = ''  # aula fica disponível para possiveis opções no decorrer da rota

    lista_alunos = list(Aluno.objects.filter(al_turma=au_turma))
    cont_iter = cont
    lista = lista_alunos[-1].id_aluno
    while cont_iter <= lista:
        try:
            alunos_turma[cont_iter] = lista_alunos[cont_iter - 1].id_aluno
            cont_iter += 1
        except:
            cont_iter += 1
    
    aluno_frequentou = ''

    # Se a aula acabou de iniciar (veio de usuario.html)
    if request.POST.get('iniciar') == 'iniciar':
        lista_presenca = ''
        if request.POST.get('nro') == '':
            nro = 0 + 1
        else:
            nro = int(request.POST.get('nro')) + 1
        Aula.objects.create(id_aula=nro, au_turma=au_turma, au_disciplina=au_disciplina)
        aula = Aula.objects.get(id_aula=nro)
    else:
        lista_presenca = request.POST.get('lista_presenca')


    # Se o aluno estiver presente
    if request.POST.get('presente') == 'presente':
        aula = Aula.objects.get(id_aula=request.POST.get('nro'))  # RECEBE ID_AULA
        alunoid = 1 if not request.POST.get('alunoid') else request.POST.get('alunoid')
        aluno = Aluno.objects.get(id_aluno=alunoid)  # SELECIONA ALUNO
        presenca = Presenca.objects.create(
            id_aula=aula,
            id_presenca=True,
        )
        presenca.id_aluno.add(aluno)
        presenca.save()
        lista_presenca += f' {presenca.id}'


    # Se o aluno faltar
    if request.POST.get('falta') == 'falta':
        aula = Aula.objects.get(id_aula=request.POST.get('nro'))  # RECEBE ID_AULA
        alunoid = 1 if not request.POST.get('alunoid') else request.POST.get('alunoid')
        aluno = Aluno.objects.get(id_aluno=alunoid)  # SELECIONA ALUNO
        presenca = Presenca.objects.create(
            id_aula=aula,
        )
        presenca.id_aluno.add(aluno)
        presenca.save()
        lista_presenca += f' {presenca.id}'

    # Ação de desfazer
    if request.POST.get('desfazer') == 'desfazer':
        if lista_presenca:
            lista = lista_presenca.split()
            ultimo_presenca = lista.pop()
            lista_presenca = ' '.join(lista)
        if request.POST.get('comeco') == 'comeco':
            return redirect('/user/')
        aula = Aula.objects.get(id_aula=request.POST.get('nro'))
        presenca = Presenca.objects.get(id=ultimo_presenca)
        presenca.delete()

    # chamando aluno
    alunos = list(Aluno.objects.filter(al_turma=au_turma))
    try:
        it = cont
        aluno_atual = alunos_turma[it]
    except:
        aluno_atual = ''
        pass

    response = {
        'aluno_atual': aluno_atual,
        'alunos': alunos,
        'aula': aula,
        'cont': cont,
        'lista_presenca': lista_presenca,
    }
    return render(request, 'chamada.html', response)


@login_required(login_url='login/')
def ver_turma(request):
    turma = None
    if request.POST.get('veral'):
        try:
            al_teste = Aluno.objects.filter(al_nome=request.POST.get('veral'))[0]
        except:
            return redirect('/not-found')
        aluno = Aluno.objects.filter(al_nome=request.POST.get('veral'))[0]
        turma = aluno.al_turma
        if request.POST.get('dis'):
            dis = Disciplina.objects.get(d_nome=request.POST.get('dis'))
            disciplina = '-'.join(dis.d_nome.split())
            aula = Aula.objects.filter(au_disciplina=dis) 
            ident = aluno.id_aluno
            presente = Presenca.objects.filter(id_aluno=ident, id_presenca=True).filter(id_aula=aula[0]).count()
            falta = Presenca.objects.filter(id_aluno=ident, id_presenca=False).filter(id_aula=aula[0]).count()
        else:
            disciplina = 'Todas-Disciplinas'
            ident = aluno.id_aluno
            presente = Presenca.objects.filter(id_aluno=ident, id_presenca=True).count()
            falta = Presenca.objects.filter(id_aluno=ident, id_presenca=False).count()
        return redirect(f'turma/aluno/{ident}/{disciplina}')
    else:
        try:
            t_teste = Turma.objects.get(t_turma=request.POST.get('vert'))
        except:
            return redirect('/not-found')
        if request.POST.get('dis') != '':
            try:
                d_teste = '' if request.POST.get('dis') == 'Todas-Disciplinas' else Disciplina.objects.filter(d_nome=request.POST.get('dis'))
                a_teste = Aula.objects.filter(au_disciplina=d_teste[0]) if d_teste != 'Todas-Disciplinas' else ''
            except:
                return redirect('/not-found')
        path = os.path.expanduser('~')
        path += '/lista-chamada.txt'
        if request.POST.get('salvar'):
            with open(path, 'w') as archive:
                if request.POST.get('dis') == '':
                    archive.write(f'Turma: {Turma.objects.get(t_turma=request.POST.get("vert"))}  |  Disciplina: Geral.\n\n\n')
                else:
                    archive.write(f'Turma: {Turma.objects.get(t_turma=request.POST.get("vert"))}  |  Disciplina: {Disciplina.objects.get(d_nome=request.POST.get("dis"))} \n\n\n')
        turma = Turma.objects.get(t_turma=request.POST.get('vert'))
        alunos = list(Aluno.objects.filter(al_turma=turma))
        consultas = []
        salvar = ''
        dis = request.POST.get('dis')
        for aluno in alunos:
            ident = aluno.id_aluno
            if dis != '':
                materia_dada = ''
                disciplina = Disciplina.objects.filter(d_nome=dis)
                aula = Aula.objects.filter(au_disciplina=disciplina[0])
                presencas = Presenca.objects.filter(id_aluno=ident)
                maior = aula.count() if aula.count() > presencas.count() else presencas.count()
                presente, falta = 0, 0
                for i in range(maior):
                    try:
                        if presencas[i].id_aula in aula:
                            if presencas[i].id_presenca:
                                presente += 1
                            else:
                                falta += 1
                    except:
                        continue
            else:
                aulas = Aula.objects.all()
                presencas = Presenca.objects.filter(id_aluno=ident)
                maior = aulas.count() if aulas.count() > presencas.count() else presencas.count()
                presente, falta = 0, 0
                materia_dada = []
                for i in range(maior):
                    if presencas[i].id_aula in aulas:
                        for au in aulas:
                            if au == presencas[i].id_aula:
                                materia_dada.append(au.au_disciplina)
                        if presencas[i].id_presenca:
                            presente += 1
                        else:
                            falta += 1
            relatorio = {
                'aluno': aluno,
                'presente': presente,
                'falta': falta,}
            if request.POST.get('salvar'):
                with open(path, 'a') as archive:
                    archive.write(f'Aluno(a): {aluno.al_nome}  |  Presenças: {presente}  |  Faltas: {falta}\n' + ('=' * 100) + '\n\n')
                salvar = 'Documento salvo em Meus documentos com o nome: lista-chamada.txt'
            consultas.append(relatorio)
        if dis == '':
            dis = 'Todas Disciplinas'
        mat = '-'.join(dis.split())
        dados = {
            'mat': mat,
            'dis': dis,
            'consultas': consultas,
            'vert': turma,
            'salvar': salvar,
        }
        return render(request, 'consulta-turma.html', dados)


@login_required(login_url='login/')
def ver_aluno(request, identificacao=0, disciplina=''):
    ident = identificacao
    dis = ''
    for palavra in disciplina.split('-'):
        dis += palavra + ' '
    dis = dis.strip()
    aluno = Aluno.objects.get(id_aluno=ident)
    # presencas = list(Presenca.objects.filter(id_aluno=ident))
    presencas = Presenca.objects.filter(id_aluno=ident)
    falta = Presenca.objects.filter(id_aluno=ident, id_presenca=False).count()
    porcentagem = (falta * 100) / presencas[0].qte_aulas
    disciplinas = [d.d_nome for d in Disciplina.objects.all()]
    aulas = Aula.objects.all()
    maior = aulas.count() if aulas.count() > presencas.count() else presencas.count()
    lista_presencas = []
    if dis in disciplinas:
        for i in range(maior):
            try:
                if presencas[i].id_aula in aulas:
                    for au in aulas:
                        if au.au_disciplina.d_nome == dis:
                            if au == presencas[i].id_aula:
                                dado = [presencas[i], au.au_disciplina]
                                lista_presencas.append(dado)
            except:
                continue
    else:
        for i in range(maior):
            for au in aulas:
                if au == presencas[i].id_aula:
                    dado = [presencas[i], au.au_disciplina]
                    lista_presencas.append(dado)
                    
    dados = {
        'dis': dis,
        'disciplinas': disciplinas,
        'aluno': aluno,
        'presenca': lista_presencas,
        'porcentagem': porcentagem,
    }
    return render(request, 'ver-aluno.html', dados)


@login_required(login_url='login/')
def user_content(request):
    aulas = Aula.objects.all().count()
    dado = {
        'nro': aulas,
        'iniciar': 'iniciar',
    }
    return render(request, 'usuario.html', dado)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('user/')
    return render(request, 'login-content.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        user = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = authenticate(username=user, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect('/user/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='login/')
def nfound(request):
    return render(request, 'not-found.html')