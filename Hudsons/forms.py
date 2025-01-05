from django import forms
from .models import CalcRevisao
from django.contrib.auth.models import User

class CalcForm(forms.ModelForm):
    class Meta:
        model = CalcRevisao
        fields = ['name', 'tipo', 'quant_pag', 'custo_pag', 'custo_diagramacao', 'diagramacao', 'usuario']
    
    def clean(self):
        cleaned_data = super().clean()
        diagramacao = cleaned_data.get('diagramacao', False)
        custo_diagramacao = cleaned_data.get('custo_diagramacao', 0)

        if diagramacao and not custo_diagramacao:
            raise forms.ValidationError("Informe o custo da diagramação.")
        if not diagramacao:
            cleaned_data['custo_diagramacao'] = 0  # Define como nulo se não houver diagramação.

        return cleaned_data

    # Campos do formulário
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    tipo = forms.ChoiceField(
        choices=[
            ('tcc', 'TCC'),
            ('dissertacao', 'Dissertação'),
            ('tese', 'Tese'),
            ('outros', 'Outros'),
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )
    quant_pag = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'required': 'required'}))
    custo_pag = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'required': 'required'}))
    diagramacao = forms.BooleanField(
        required=False, 
        initial=False,  # Define o valor padrão como False
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    custo_diagramacao = forms.FloatField(
        required=False,  # Torna o campo não obrigatório
        initial=0,  # Define o valor padrão como 0
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
    )
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        required=False  # Opcional caso o usuário não esteja logado
    )