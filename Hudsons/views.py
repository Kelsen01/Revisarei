from django.shortcuts import render, get_object_or_404, redirect
from .models import CalcRevisao
from .forms import CalcForm
from django.http import JsonResponse
from django.db.models import Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from urllib.parse import urlparse
import locale
from datetime import datetime
from django.db.models import Count
from django.db.models import Q

# Create your views here.
def index(request):
    # Obter lista de cálculos existentes
    calcs = CalcRevisao.objects.all().order_by('-data')
    
    # Obter tipos com a contagem de registros
    tipos_com_total = (
        CalcRevisao.objects
        .values("tipo")
        .annotate(total=Count("id"))
        .filter(total__gt=10)  # Filtra tipos com mais de 10 resultados
        .order_by("tipo")
        .values_list("tipo", flat=True)
    )
    
    tipos = CalcRevisao.objects.values_list('tipo', flat=True).distinct().order_by('tipo')
    
    user_id = request.user.id if request.user.is_authenticated else None
    user_name = request.user.get_username() if request.user.is_authenticated else ""

    # Paginação: limite de 12 resultados por página
    paginator = Paginator(calcs, 12)
    page_number = request.GET.get('page')  # Número da página na URL
    page_obj = paginator.get_page(page_number)  # Objeto da página atual

    # Se for uma requisição POST, tenta criar um novo cálculo
    if request.method == 'POST':
        form = CalcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # Redireciona para a própria página após salvar
    else:
        form = CalcForm()

    context = {
        'page_obj': page_obj,
        'form': form,
        'tipos': tipos,  # Apenas tipos com mais de 10 resultados
        'user_id': user_id,
        'user_name': user_name,
    }
    
    return render(request, 'Hudsons/index.html', context)

@login_required #só pode ser utilizada por quem está logado
def CalcView(request, id):
    Calc = get_object_or_404(CalcRevisao, pk=id)
    return render(request, '#', {'calcs':Calc}) #coloque o html do calculo da pessoa, servira para procurar pelo id do calc e levar ate a informacao dele (video 09 do Matheus Battisti)

def calcular_medias(request):
    if request.method == "GET":
        tipo = request.GET.get("tipo")
        user_id = request.user.id if request.user.is_authenticated else None
        referer = request.META.get("HTTP_REFERER", "")
        referer_path = urlparse(referer).path

        # Verifica se a chamada veio de "perfil.html"
        if referer_path.endswith("/perfil/") and user_id:
            # Filtra apenas os cálculos do usuário logado
            servicos = CalcRevisao.objects.filter(usuario=user_id)
        else:
            # Filtra todos os cálculos
            servicos = CalcRevisao.objects.all()

        if tipo:
            servicos = servicos.filter(tipo=tipo)

        quantidade = servicos.count()

        if quantidade > 0:
            media_paginas = servicos.aggregate(avg_paginas=Avg("quant_pag"))["avg_paginas"] or 0
            media_custo_pagina = servicos.aggregate(avg_custo_pagina=Avg("custo_pag"))["avg_custo_pagina"] or 0
            media_diagramacao = servicos.aggregate(avg_diagramacao=Avg("custo_diagramacao"))["avg_diagramacao"] or 0
            media_total = servicos.aggregate(avg_custo=Avg("custo"))["avg_custo"] or 0

            return JsonResponse({
                "media_paginas": round(media_paginas, 2),
                "media_custo_pagina": round(media_custo_pagina, 2),
                "media_diagramacao": round(media_diagramacao, 2),
                "media_total": round(media_total, 2),
                "quantidade": quantidade,
            })
        else:
            return JsonResponse({
                "message": "Nenhum dado encontrado para o tipo selecionado."
            }, status=404)
    else:
        return JsonResponse({
            "message": "Método não suportado."
        }, status=405)
            
@login_required  # só pode ser utilizada por quem está logado
def perfil(request):
    user_id = request.user.id

    # Configura o locale para português do Brasil
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Obter cálculos do usuário
    calcs = CalcRevisao.objects.filter(usuario=user_id).order_by('-id')

    tipos = (
    CalcRevisao.objects.filter(usuario=user_id)  # Filtra os registros pelo usuário
    .values("tipo")                              # Agrupa pelos tipos
    .annotate(total=Count("id"))                 # Adiciona a contagem de registros por tipo
    .filter(total__gt=0)                         # Filtra apenas os tipos com total maior que 0
    .order_by("tipo")                            # Ordena alfabeticamente
    .values_list("tipo", flat=True)              # Retorna apenas os nomes dos tipos
    )  

    campo = request.GET.get('campo', '')
    operador = request.GET.get('operador', '')
    valor = request.GET.get('valor', '')

    if campo and operador and valor:
        if operador == 'maior':
            filtros = {f"{campo}__gt": valor}
        elif operador == 'menor':
            filtros = {f"{campo}__lt": valor}

        calcs = calcs.filter(**filtros)
    elif campo == 'tipo':
        tipo = request.GET.get('tipo')
        if tipo:
            calcs = calcs.filter(tipo=tipo)


    # Agrupar por mês
    monthly_data = (
        calcs.annotate(month=TruncMonth('data'))  # Supondo que existe o campo "data_criacao"
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

     # Preparar dados para o gráfico (para o gráfico de todas as atividades, sem filtro)
    all_monthly_data = (
        CalcRevisao.objects.filter(usuario=user_id)  # Todos os cálculos do usuário
        .annotate(month=TruncMonth('data'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    
    months = [item['month'].strftime('%B') for item in all_monthly_data]  # Meses de todas as atividades
    totals = [item['total'] for item in all_monthly_data]  # Totais de todas as atividades

    # Paginação
    paginator = Paginator(calcs, 12)
    page_number = request.GET.get('page')  # Número da página na URL
    page_obj = paginator.get_page(page_number)  # Objeto da página atual

    context = {
        'page_obj': page_obj,
        'months': months,
        'totals': totals,
        'tipos': tipos,
        'campo_selecionado': campo,
        'operador_selecionado': operador,
        'valor_selecionado': valor,
    }

    return render(request, 'Hudsons/perfil.html', context)

@login_required
def calcular_medias_usuario(request):
    user_id = request.user.id

    # Obter cálculos do usuário
    calcs = CalcRevisao.objects.filter(usuario=user_id)

    # Verifica se há cálculos para o usuário
    if calcs.exists():
        media_paginas = calcs.aggregate(avg_paginas=Avg("quant_pag"))["avg_paginas"] or 0
        media_custo_pagina = calcs.aggregate(avg_custo_pagina=Avg("custo_pag"))["avg_custo_pagina"] or 0
        media_diagramacao = calcs.aggregate(avg_diagramacao=Avg("custo_diagramacao"))["avg_diagramacao"] or 0
        media_total = calcs.aggregate(avg_custo=Avg("custo"))["avg_custo"] or 0

        return JsonResponse({
            "media_paginas": round(media_paginas, 2),
            "media_custo_pagina": round(media_custo_pagina, 2),
            "media_diagramacao": round(media_diagramacao, 2),
            "media_total": round(media_total, 2),
        })

    return JsonResponse({
        "message": "Nenhum dado encontrado para o usuário."
    }, status=404)


def sobre(request):
    return render(request, 'Hudsons/sobre.html')