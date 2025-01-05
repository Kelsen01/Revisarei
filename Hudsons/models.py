from django.db import models
from django.contrib.auth.models import User

class CalcRevisao(models.Model):
    #Informações dos calculos de revisao
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Chave estrangeira para Usuario
    name = models.CharField(max_length=40)
    tipo = models.CharField(max_length=50, choices=[
        ('tcc', 'TCC'),
        ('dissertacao', 'Dissertação'),
        ('tese','Tese'),
        ('outros','Outros'),
    ])
    quant_pag = models.IntegerField()
    custo_pag = models.FloatField()
    diagramacao = models.BooleanField()
    custo_diagramacao = models.FloatField(null=True, blank=True, default=0.0)
    custo = models.FloatField(default=0.0)
    data = models.DateTimeField(auto_now=True)
    
    def calcular_custo(self):
        #Calcula o custo total com base nos campos do modelo.
        custo_diagramacao_valor = self.custo_diagramacao if self.diagramacao and self.custo_diagramacao else 0.0
        return (self.quant_pag * self.custo_pag) + custo_diagramacao_valor

    def save(self, *args, **kwargs):
        # Atualiza o custo antes de salvar no banco de dados
        self.custo = self.calcular_custo()
        
        # Garante que custo_diagramacao seja 0 se diagramacao for False
        if not self.diagramacao:
            self.custo_diagramacao = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.tipo} - {self.quant_pag} páginas - Custo total: R${self.custo:.2f}"
    
