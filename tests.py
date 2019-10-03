from django.test import TestCase, Client
from shortener_url.models import Url
from rest_framework import status
import json

class TestUrl(TestCase):

    def setUp(self):
        Url.objects.create(original_url="https://web.whatsapp.com/", custom_alias="whatsapp", short_url="http://shortener/u/whatsapp")

    def test_visited_url(self):
        response = self.client.get('/visited')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_shortener_alias(self):
        data = {
            'url': 'http://www.google.com.br', 
            'CUSTOM_ALIAS': 'google'
        }
        response = self.client.post('/create', json.dumps(data), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_shortener_without_url(self):
        data = {
            'url': '', 
            'CUSTOM_ALIAS': ''
        }
        response = self.client.post('/create', json.dumps(data), content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_shortener(self):
        data = {
            'url': 'https://www.youtube.com/', 
            'CUSTOM_ALIAS': ''
        }
        response = self.client.post('/create', json.dumps(data), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)



    def test_shortener_existing_alias(self):
        data = {
            'url': 'https://web.whatsapp.com/', 
            'CUSTOM_ALIAS': 'whatsapp'
        }
        response = self.client.post('/create', json.dumps(data), content_type="application/json").json()
        self.assertEqual('001', response['err_code'])


    def test_retrieve_url(self):
        response = self.client.get('/?url=http://shortener/u/whatsapp')
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_retrieve_url_not_found(self):
        response = self.client.get('/?url=http://shortener/u/gmail').json()
        self.assertEqual('002', response['err_code'])

    def test_retrieve_without_url(self):
        response = self.client.get('/')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)