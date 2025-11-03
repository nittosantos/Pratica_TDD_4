from django.test import TestCase
from core.forms import AgendaForm
from core.models import Agenda


class AgendaFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nome_completo': 'John Doe',
            'telefone': '(19) 99999-8888',
            'email': 'john.doe@example.com',
            'observacao': 'Test contact'
        }

    def test_form_has_fields(self):
        form = AgendaForm()
        expected_fields = ['nome_completo', 'telefone', 'email', 'observacao']
        self.assertSequenceEqual(expected_fields, list(form.fields))

    def test_form_is_valid_with_valid_data(self):
        form = AgendaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_nome_completo_is_required(self):
        data = self.valid_data.copy()
        data['nome_completo'] = ''
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome_completo', form.errors)

    def test_telefone_is_required(self):
        data = self.valid_data.copy()
        data['telefone'] = ''
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_email_is_required(self):
        data = self.valid_data.copy()
        data['email'] = ''
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_must_be_valid(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_observacao_is_optional(self):
        data = self.valid_data.copy()
        data['observacao'] = ''
        form = AgendaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_saves_contact(self):
        form = AgendaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertIsInstance(contact, Agenda)
        self.assertEqual(contact.nome_completo, 'John Doe')
        self.assertEqual(contact.telefone, '(19) 99999-8888')
        self.assertEqual(contact.email, 'john.doe@example.com')
        self.assertEqual(contact.observacao, 'Test contact')

    def test_telefone_with_only_letters_is_invalid(self):
        data = self.valid_data.copy()
        data['telefone'] = 'asdfasdfasdfadf'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_telefone_with_letters_and_numbers_is_invalid(self):
        data = self.valid_data.copy()
        data['telefone'] = '123abc456'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_telefone_with_less_than_10_digits_is_invalid(self):
        data = self.valid_data.copy()
        data['telefone'] = '123456789'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_telefone_with_more_than_11_digits_is_invalid(self):
        data = self.valid_data.copy()
        data['telefone'] = '123456789012'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)

    def test_telefone_with_valid_formats(self):
        valid_phones = [
            '(19) 99999-8888',
            '19999998888',
            '19 99999 8888',
            '199999-8888',
            '(19)999998888',
            '1999999888',  # 10 dígitos (telefone fixo)
            '11999998888',  # 11 dígitos (celular)
        ]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                data = self.valid_data.copy()
                data['telefone'] = phone
                form = AgendaForm(data=data)
                self.assertTrue(form.is_valid(), f"Telefone {phone} deveria ser válido")
