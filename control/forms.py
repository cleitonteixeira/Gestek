from django import forms
from .models import ClasseEquipamento, Equipamento, Manutencao, Unidade
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserFullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username

class UnidadeForm(forms.ModelForm):
    gu = UserFullNameChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Gerente da Unidade (GU)"
    )
    supervisor = UserFullNameChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Supervisor"
    )

    class Meta:
        model = Unidade
        fields = ['nome', 'gu', 'supervisor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nutribem Centro'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gu'].queryset = User.objects.order_by('first_name', 'last_name')
        self.fields['supervisor'].queryset = User.objects.order_by('first_name', 'last_name')

class EditUnidadeForm(forms.ModelForm):
    gu = UserFullNameChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Gerente da Unidade (GU)"
    )
    supervisor = UserFullNameChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Supervisor"
    )

    class Meta:
        model = Unidade
        fields = ['nome', 'gu', 'supervisor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nutribem Centro'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gu'].queryset = User.objects.order_by('first_name', 'last_name')
        self.fields['supervisor'].queryset = User.objects.order_by('first_name', 'last_name')


class EquipamentoForm(forms.ModelForm):
    classe = forms.ModelChoiceField(
        queryset=ClasseEquipamento.objects.all(),
        label="Classe de Equipamento",
        empty_label="Selecione uma Classe",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_classe'})
    )
    class Meta:
        model = Equipamento
        fields = ['nome', 'unidade', 'classe', 'tipo','valor','responsavel', 'status', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Liquidificador Industrial'}),
            'unidade': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: João da Silva'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se estiver editando um equipamento, pré-seleciona a classe dele
        if self.instance.pk and self.instance.tipo:
            self.fields['classe'].initial = self.instance.tipo.classe
        
class TransferenciaEquipamentoForm(forms.ModelForm):
    motivo = forms.CharField(
        label="Motivo / Observação",
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px', 'placeholder': 'Descreva o motivo da transferência'}),
        required=True
    )

    class Meta:
        model = Equipamento
        fields = ['unidade', 'responsavel']
        widgets = {
            'unidade': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.unidade:
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.exclude(
                pk=self.instance.unidade.pk
            )

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário:", max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Nome de usuário"}))
    password = forms.CharField(label="Senha:",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Senha"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Nome de usuário ou senha inválidos.")
        return cleaned_data
    
class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['data_manutencao', 'tipo', 'descricao', 'prestador', 'valor', 'proxima_manutencao']
        widgets = {
            'data_manutencao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proxima_manutencao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'O que foi feito?'}),
            'prestador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa ou técnico'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }