from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from http import HTTPStatus
from core.models import Agenda
from core.forms import AgendaForm


class CreateContactTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@fatec.sp.gov.br',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('create_contact')

    def test_create_contact_get_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_contact_get_returns_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_contact.html')
        self.assertIsInstance(response.context['form'], AgendaForm)

    def test_create_contact_post_valid_data(self):
        data = {
            'nome_completo': 'John Doe',
            'telefone': '(19) 99999-8888',
            'email': 'john@example.com',
            'observacao': 'Test contact'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('list_contacts'))
        self.assertTrue(Agenda.objects.filter(nome_completo='John Doe').exists())

    def test_create_contact_post_invalid_data(self):
        data = {
            'nome_completo': '',
            'telefone': '',
            'email': 'invalid-email'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'create_contact.html')
        self.assertFalse(Agenda.objects.exists())


class ListContactsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@fatec.sp.gov.br',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('list_contacts')
        self.contact1 = Agenda.objects.create(
            nome_completo='John Doe',
            telefone='(19) 99999-8888',
            email='john@example.com'
        )
        self.contact2 = Agenda.objects.create(
            nome_completo='Jane Smith',
            telefone='(19) 99999-7777',
            email='jane@example.com'
        )

    def test_list_contacts_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_list_contacts_displays_all_contacts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'list_contacts.html')
        self.assertIn(self.contact1, response.context['contacts'])
        self.assertIn(self.contact2, response.context['contacts'])
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')

    def test_list_contacts_empty_list(self):
        Agenda.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['contacts']), 0)


class UpdateContactTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@fatec.sp.gov.br',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.contact = Agenda.objects.create(
            nome_completo='John Doe',
            telefone='(19) 99999-8888',
            email='john@example.com',
            observacao='Old notes'
        )

    def test_update_contact_get_requires_login(self):
        self.client.logout()
        url = reverse('update_contact', args=[self.contact.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_contact_get_returns_form_with_data(self):
        url = reverse('update_contact', args=[self.contact.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'update_contact.html')
        self.assertIsInstance(response.context['form'], AgendaForm)
        self.assertEqual(response.context['form'].instance, self.contact)

    def test_update_contact_post_valid_data(self):
        url = reverse('update_contact', args=[self.contact.id])
        data = {
            'nome_completo': 'John Updated',
            'telefone': '(19) 88888-7777',
            'email': 'john.updated@example.com',
            'observacao': 'Updated notes'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('list_contacts'))
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.nome_completo, 'John Updated')
        self.assertEqual(self.contact.telefone, '(19) 88888-7777')
        self.assertEqual(self.contact.email, 'john.updated@example.com')
        self.assertEqual(self.contact.observacao, 'Updated notes')

    def test_update_contact_post_invalid_data(self):
        url = reverse('update_contact', args=[self.contact.id])
        data = {
            'nome_completo': '',
            'telefone': '',
            'email': 'invalid-email'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'update_contact.html')
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.nome_completo, 'John Doe')

    def test_update_contact_404_not_found(self):
        url = reverse('update_contact', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class DeleteContactTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@fatec.sp.gov.br',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.contact = Agenda.objects.create(
            nome_completo='John Doe',
            telefone='(19) 99999-8888',
            email='john@example.com'
        )

    def test_delete_contact_requires_login(self):
        self.client.logout()
        url = reverse('delete_contact', args=[self.contact.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_contact_post_deletes_contact(self):
        url = reverse('delete_contact', args=[self.contact.id])
        contact_id = self.contact.id
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('list_contacts'))
        self.assertFalse(Agenda.objects.filter(id=contact_id).exists())

    def test_delete_contact_404_not_found(self):
        url = reverse('delete_contact', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
