from django.db import models

# Create your models here.

class Classes(models.Model):

    nome = models.CharField(max_length=100,unique=True)

class Recursos(models.Model):

    codigo=models.CharField(max_length=100, unique=True)
    descricao=models.CharField(max_length=255)

class Pecas(models.Model):

    TIPO_CHOICES = (('peca','Peça'),('conjunto','Conjunto'))

    codigo = models.CharField(max_length=10, unique=True)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='pecas')
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=10, default='Un')
    class_fiscal = models.CharField(max_length=20, default='8716.90.90')
    procedencia = models.CharField(max_length=50, default='Nacional - 0')
    status = models.TextField()
    tipo = models.CharField(choices=TIPO_CHOICES)
    
class BlocoEtapas(models.Model):
    DESTINO_CHOICES = [
        ('almox_pintura_embalagem', 'Almox Pintura'),
        ('almox_prod_especiais', 'Almox Prod Especiais'),
        ('almox_cx_acessorios', 'Almox Cx Acessórios'),
        ('almox_carpintaria', 'Almox Carpintaria'),
        ('almox_central', 'Almox Central'),
        ('almox_qualidade', 'Almox Qualidade'),
        ('almox_corte_estamparia', 'Almox Corte e Estamparia'),
        ('almox_prototipos', 'Almox Protótipos'),
        ('almox_serra', 'Almox Serra'),
    ]

    PROCESSO_CHOICES = [
        ('s_c_plasma', 'S C Plasma'),
        ('s_c_guilhotina', 'S C Guilhotina'),
        ('s_c_laser', 'S C Laser'),
        ('s_c_prensas', 'S C Prensas'),
        ('s_c_serras', 'S C Serras'),
        ('s_carpintaria', 'S Carpintaria'),
        ('s_corte_manual', 'S Corte Manual'),
        ('s_cx_acessorios', 'S Cx Acessórios'),
        ('s_desbobinar', 'S Desbobinar'),
        ('s_estamparia', 'S Estamparia'),
        ('s_expedicao', 'S Expedição'),
        ('s_forjaria', 'S Forjaria'),

    ]

    peca = models.ForeignKey(Pecas, related_name='etapas', on_delete=models.CASCADE)
    ordem = models.IntegerField()
    processo = models.CharField(choices=PROCESSO_CHOICES, max_length=50)
    descricao = models.CharField(max_length=20)
    destino = models.CharField(choices=DESTINO_CHOICES, max_length=50)
    desvio = models.CharField(choices=DESTINO_CHOICES, max_length=50)

class BlocoRecursos(models.Model):
    DEPOSITO_ORIGEM_CHOICES = [
        ('almox_pintura_embalagem', 'Almox Pintura'),
        ('almox_prod_especiais', 'Almox Prod Especiais'),
        ('almox_cx_acessorios', 'Almox Cx Acessórios'),
        ('almox_carpintaria', 'Almox Carpintaria'),
        ('almox_central', 'Almox Central'),
        ('almox_qualidade', 'Almox Qualidade'),
        ('almox_corte_estamparia', 'Almox Corte e Estamparia'),
        ('almox_prototipos', 'Almox Protótipos'),
        ('almox_serra', 'Almox Serra'),
    ]

    peca = models.ForeignKey(Pecas, related_name='recursos', on_delete=models.CASCADE)
    ordem = models.IntegerField()
    recurso = models.ForeignKey(Recursos, on_delete=models.CASCADE, related_name='codigo_recursos')
    quantidade = models.FloatField()
    dep_origem = models.CharField(choices=DEPOSITO_ORIGEM_CHOICES, max_length=50)
    obs = models.CharField(max_length=100)
    flag_romaneio = models.BooleanField(default=False)
    cx_acess = models.BooleanField(default=False)

class BlocoPropriedade(models.Model):
    PROP_CHOICES = [
        ('comprimento', 'Comprimento')
    ]

    peca = models.ForeignKey(Pecas, related_name='propriedades', on_delete=models.CASCADE)
    propriedade = models.CharField(max_length=20, choices=PROP_CHOICES)
    valor = models.FloatField()


    
