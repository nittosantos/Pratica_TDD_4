import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from core.models import Agenda

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-Mail:',
            'password': 'Senha:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail institucional'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder':'Digite sua senha'}),
        }
        error_messages = {
            'email': {
                'required': ("Informe o e-mail."),
            },
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@fatec.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Usuário com esse e-mail não encontrado.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Senha incorreta para o e-mail informado.")

            self.user = user


class AgendaForm(ModelForm):
    class Meta:
        model = Agenda
        fields = ('nome_completo', 'telefone', 'email', 'observacao')
        labels = {
            'nome_completo': 'Nome Completo:',
            'telefone': 'Telefone:',
            'email': 'E-Mail:',
            'observacao': 'Observação:',
        }
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: (19) 99999-8888 ou 19999998888'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o e-mail'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite observações (opcional)'
            }),
        }
        error_messages = {
            'nome_completo': {
                'required': 'O nome completo é obrigatório.',
            },
            'telefone': {
                'required': 'O telefone é obrigatório.',
            },
            'email': {
                'required': 'O e-mail é obrigatório.',
                'invalid': 'Informe um endereço de e-mail válido.',
            },
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Verifica se contém apenas caracteres válidos (dígitos, parênteses, traços, espaços)
            if not re.match(r'^[\d\s\(\)\-]+$', telefone):
                raise ValidationError('O telefone deve conter apenas números e caracteres especiais permitidos ((), -, espaços).')

            # Remove caracteres especiais para contar apenas os dígitos
            telefone_limpo = re.sub(r'[^\d]', '', telefone)

            # Verifica se tem pelo menos alguns dígitos
            if not telefone_limpo:
                raise ValidationError('O telefone deve conter pelo menos alguns números.')

            # Verifica o tamanho mínimo (10 dígitos para telefone fixo) e máximo (11 dígitos para celular)
            if len(telefone_limpo) < 10:
                raise ValidationError('O telefone deve ter no mínimo 10 dígitos.')

            if len(telefone_limpo) > 11:
                raise ValidationError('O telefone deve ter no máximo 11 dígitos.')

        return telefone