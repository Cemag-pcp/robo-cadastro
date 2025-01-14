from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar-peca/', views.cadastrar_peca, name='cadastrar_peca'),
    path('cadastrar-conjunto/', views.cadastrar_conjunto, name='cadastrar_conjunto'),

    path('peca-sucesso/', views.peca_sucesso, name='peca_sucesso'),
    path('conjunto-sucesso/', views.conjunto_sucesso, name='conjunto_sucesso'),

    path('acompanhamento/', views.acompanhamento, name='acompanhamento'),

    path('api/etapas/<int:pk>/', views.solicitacao_detalhes, name='solicitacao_detalhes'),
    path('api/recursos/<int:pk>/', views.detalhes_recursos, name='detalhes_recursos'),
    path('api/propriedades/<int:pk>/', views.detalhes_propriedades, name='detalhes_propriedades'),
    path('api/etapas-choices/', views.get_etapas_choices, name='etapas_choices'),
    path('api/recursos/', views.get_recursos, name='get_recursos'),

    path('gerar-json/pecas', views.gerar_json_view_pecas, name='gerar_json_view_pecas'),
    path('gerar-json/conjuntos', views.gerar_json_view_conjuntos, name='gerar_json_view_conjuntos'),
    path('registrar-status/', views.registrar_status, name='registrar_status'),

    # Cadastros gerais
    path('cadastrar-classe/', views.cadastrar_classe, name='cadastrar_classe'),

]
