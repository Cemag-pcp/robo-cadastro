from django.shortcuts import render, redirect
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Classes, Pecas, BlocoEtapas, BlocoRecursos, BlocoPropriedade, Recursos

import json
from collections import defaultdict

def cadastrar_peca(request):
    if request.method == 'POST':
        print(request.POST)

        with transaction.atomic():
            # Captura os dados da peça
            codigo = request.POST.get('codigo')
            nome = request.POST.get('nome')
            classe_id = request.POST.get('classe')
            
            # Cria a peça
            classe = Classes.objects.get(id=classe_id)
            peca = Pecas.objects.create(codigo=codigo, nome=nome, classe=classe, tipo='peca')
            
            # Captura as etapas dinâmicas
            etapas_descricao = request.POST.getlist('descricao')
            etapas_processo = request.POST.getlist('processo')
            etapas_destino = request.POST.getlist('destino')
            etapas_desvio = request.POST.getlist('desvio')
            for i in range(len(etapas_descricao)):
                BlocoEtapas.objects.create(
                    peca=peca,
                    ordem=i + 1,
                    descricao=etapas_descricao[i],
                    processo=etapas_processo[i],
                    destino=etapas_destino[i],
                    desvio=etapas_desvio[i]
                )
            
            # Captura os recursos dinâmicos
            recursos_nome = request.POST.getlist('recurso')
            recursos_quantidade = request.POST.getlist('quantidade')
            recursos_dep_origem = request.POST.getlist('dep_origem')
            for i in range(len(recursos_nome)):
                BlocoRecursos.objects.create(
                    peca=peca,
                    ordem=i + 1,
                    recurso=get_object_or_404(Recursos, codigo=recursos_nome[i]),
                    quantidade=float(recursos_quantidade[i]),
                    dep_origem=recursos_dep_origem[i],
                )
            
            # Captura as propriedades dinâmicas
            propriedades_nome = request.POST.getlist('propriedade')
            propriedades_valor = request.POST.getlist('valor')
            for i in range(len(propriedades_nome)):
                BlocoPropriedade.objects.create(
                    peca=peca,
                    propriedade=propriedades_nome[i],
                    valor=float(propriedades_valor[i])
                )
            
            # Redireciona após o cadastro
            return redirect('peca_sucesso')  # Ajuste o nome da URL conforme necessário

    # Carrega as classes para exibição no formulário
    classes = Classes.objects.all()
    return render(request, 'cadastro-peca.html', {'classes': classes})

def cadastrar_conjunto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            with transaction.atomic():
                # Captura os dados da peça
                codigo = data.get('codigo')
                nome = data.get('nome')
                classe_id = data.get('classe')

                # Valida a classe
                classe = get_object_or_404(Classes, id=classe_id)

                # Cria a peça
                peca = Pecas.objects.create(codigo=codigo, nome=nome, classe=classe, tipo='conjunto')

                # Captura as etapas dinâmicas
                etapas = data.get('etapas', [])
                for i, etapa in enumerate(etapas):
                    BlocoEtapas.objects.create(
                        peca=peca,
                        ordem=i + 1,
                        descricao=etapa.get('descricao'),
                        processo=etapa.get('processo'),
                        destino=etapa.get('destino'),
                        desvio=etapa.get('desvio')
                    )

                # Captura os recursos dinâmicos
                recursos = data.get('recursos', [])
                for i, recurso in enumerate(recursos):
                    BlocoRecursos.objects.create(
                        peca=peca,
                        ordem=i + 1,
                        recurso=get_object_or_404(Recursos, codigo=recurso.get('recurso')),
                        quantidade=float(recurso.get('quantidade')),
                        dep_origem=recurso.get('depOrigem'),
                        flag_romaneio=recurso.get('flagRomaneio', 'off') == 'on', 
                        cx_acess=recurso.get('cxAcess', 'off') == 'on' 
                    )
            
                # Redireciona após o cadastro
                return JsonResponse({'message': 'Conjunto criado com sucesso!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Carrega as classes para exibição no formulário
    classes = Classes.objects.all()
    return render(request, 'cadastro-conjunto.html', {'classes': classes})

def peca_sucesso(request):

    return render(request, 'sucesso.html')

def conjunto_sucesso(request):

    return render(request, 'sucesso-conjunto.html')

def acompanhamento(request):

    solicitacoes = Pecas.objects.exclude(status='ok')

    return render(request, 'acompanhamento.html', {'solicitacoes':solicitacoes})

def solicitacao_detalhes(request, pk):
    etapas = BlocoEtapas.objects.filter(peca=pk)  # Retorna todas as etapas para a peça
    data = []
    for etapa in etapas:
        data.append({
            'id': etapa.id,
            'peca_id': etapa.peca_id,
            'ordem': etapa.ordem,
            'processo': etapa.get_processo_display(),
            'descricao': etapa.descricao,
            'destino': etapa.get_destino_display(),
            'desvio': etapa.get_desvio_display(),
        })
    return JsonResponse(data, safe=False)  # safe=False permite retornar uma lista

def detalhes_recursos(request, pk):
    recursos = BlocoRecursos.objects.filter(peca=pk)  # Retorna todas os recursos para a peça
    data = []
    for recurso in recursos:
        data.append({
            'id': recurso.id,
            'ordem': recurso.ordem,
            'recurso': recurso.recurso.codigo + " - " + recurso.recurso.descricao,
            'quantidade': recurso.quantidade,
            'dep_origem': recurso.get_dep_origem_display(),
        })
    return JsonResponse(data, safe=False)  # safe=False permite retornar uma lista

def detalhes_propriedades(request, pk):
    propriedades = BlocoPropriedade.objects.filter(peca=pk)  # Retorna todas os recursos para a peça
    data = []
    for propriedade in propriedades:
        data.append({
            'id': propriedade.id,
            'propriedade': propriedade.propriedade,
            'valor': propriedade.valor,
        })
    return JsonResponse(data, safe=False)  # safe=False permite retornar uma lista

def gerar_json_view_pecas(request):
    pecas = Pecas.objects.filter(~Q(status='ok'), tipo='peca')
    resultado = []
    for peca in pecas:
        # Informações da peça
        peca_data = {
            'codigo': peca.codigo,
            'ref_principal': peca.codigo,  # Aqui usei o mesmo valor do exemplo fornecido
            'classe': peca.classe.nome,
            'nome': peca.nome,
            'desc_generica': peca.nome,  # Usando o mesmo campo para descrição genérica
            'un': peca.unidade,
            'class_fiscal': peca.class_fiscal,
            'procedencia': peca.procedencia,
        }

        # Etapas relacionadas
        etapas_data = [
            {
                'ordem': etapa.ordem,
                'processo': etapa.get_processo_display(),
                'descricao': etapa.descricao,
                'destino': etapa.get_destino_display(),
                'desvio': etapa.get_desvio_display(),
            }
            for etapa in peca.etapas.all()
        ]

        # Recursos relacionados
        recursos_data = [
            {
                'ordem': recurso.ordem,
                'recurso': {
                    'codigo': recurso.recurso.codigo,
                    'descricao': recurso.recurso.descricao
                },
                'quantidade': recurso.quantidade,
                'dep_origem': recurso.get_dep_origem_display(),
                'flag_romaneio': recurso.flag_romaneio,
                'cx_acess': recurso.cx_acess,
            }
            for recurso in peca.recursos.all()
        ]

        # Propriedades relacionadas
        propriedades_data = [
            {
                'propriedade': propriedade.get_propriedade_display(),
                'valor': propriedade.valor,
            }
            for propriedade in peca.propriedades.all()
        ]

        # Monta o resultado final para a peça
        resultado.append({
            'peca': peca_data,
            'etapas': etapas_data,
            'recursos': recursos_data,
            'propriedades': propriedades_data,
        })

    return JsonResponse({'pecas': resultado})

def gerar_json_view_conjuntos(request):
    pecas = Pecas.objects.filter(~Q(status='ok'))
    resultado = []
    for peca in pecas:
        # Informações da peça
        peca_data = {
            'codigo': peca.codigo,
            'ref_principal': peca.codigo,  # Aqui usei o mesmo valor do exemplo fornecido
            'classe': peca.classe.nome,
            'nome': peca.nome,
            'desc_generica': peca.nome,  # Usando o mesmo campo para descrição genérica
            'un': peca.unidade,
            'class_fiscal': peca.class_fiscal,
            'procedencia': peca.procedencia,
        }

        # Etapas relacionadas
        etapas_data = [
            {
                'ordem': etapa.ordem,
                'processo': etapa.get_processo_display(),
                'descricao': etapa.get_descricao_display(),
                'destino': etapa.get_destino_display(),
                'desvio': etapa.get_desvio_display(),
            }
            for etapa in peca.etapas.all()
        ]

        # Recursos relacionados
        recursos_data = [
            {
                'ordem': recurso.ordem,
                'recurso': recurso.recurso,
                'quantidade': recurso.quantidade,
                'dep_origem': recurso.get_dep_origem_display(),
            }
            for recurso in peca.recursos.all()
        ]

        # Propriedades relacionadas
        propriedades_data = [
            {
                'propriedade': propriedade.get_propriedade_display(),
                'valor': propriedade.valor,
            }
            for propriedade in peca.propriedades.all()
        ]

        # Monta o resultado final para a peça
        resultado.append({
            'peca': peca_data,
            'etapas': etapas_data,
            'recursos': recursos_data,
            'propriedades': propriedades_data,
        })

    return JsonResponse({'pecas': resultado})

@csrf_exempt
def registrar_status(request):
    if request.method == 'POST':
        try:
            # Lê os dados enviados no corpo da requisição
            data = json.loads(request.body)

            # Extrai o status enviado
            status = data.get('status')
            codigo = data.get('codigo')

            if not status:
                return JsonResponse({'status': 'error', 'message': 'O campo "status" é obrigatório.'}, status=400)

            # Atualiza o status de todas as peças
            Pecas.objects.filter(codigo=codigo).update(status=status)

            return JsonResponse({'status': 'success', 'message': 'Status atualizado com sucesso!'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido na requisição.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erro inesperado: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

@csrf_exempt
def cadastrar_classe(request):

    classes_cadastradas = Classes.objects.all()

    if request.method=='POST':

        try:
            Classes.objects.create(
                nome=request.POST.get('nome'),
            )
        except:
            return render(request, "cadastros/classes.html", {'classes_cadastradas':classes_cadastradas})

        return render(request, "cadastros/classes.html", {'classes_cadastradas':classes_cadastradas})

    return render(request, "cadastros/classes.html", {'classes_cadastradas':classes_cadastradas})

def get_etapas_choices(request):
    return JsonResponse({
        'destino_choices': BlocoEtapas.DESTINO_CHOICES,
        'processo_choices': BlocoEtapas.PROCESSO_CHOICES
    })

def get_recursos(request):

    # Pega o termo de busca do parâmetro `search`, se existir
    search = request.GET.get('search', '')
    # Página atual (padrão é 1)
    page = int(request.GET.get('page', 1))
    # Itens por página
    per_page = 10

    # Filtra recursos com base no termo de busca (case insensitive)
    recursos = Recursos.objects.filter(
        Q(codigo__icontains=search) | Q(descricao__icontains=search)
    ).order_by('codigo')

    # Paginação
    paginator = Paginator(recursos, per_page)
    recursos_page = paginator.get_page(page)

    # Retorna os dados em formato JSON
    return JsonResponse({
        'results': [
            {'id': recurso.codigo, 'label': recurso.descricao} for recurso in recursos_page
        ],
        'next': recursos_page.has_next(),  # Se há mais páginas
    })
