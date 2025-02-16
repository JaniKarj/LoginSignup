from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse

class AuthTests(TestCase):
    def setUp(self):
        "Luodaan testikäyttäjä"
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        #Testataan että käyttäjä voi kirjautua tiedoillaan
        response = self.client.post(reverse('base:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302) #Odotetaan 302 uudelleenohjausta kirjautumisen jälkeen
        # Uudelleenohjaus kotisivulle
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)  # Varmistetaan että sivusto latautuu
        self.assertTrue(response.wsgi_request.user.is_authenticated)  #Käyttäjän pitäisi olla kirjautuneena

    def test_login_failure(self):
        #Testataan että kirjautuminen epäonnistuu epäkelvoilla tiedoilla
        response = self.client.post(reverse('base:login'), {
            'username': self.username,
            'password': 'epäkelposalasana'
        })
        
        self.assertEqual(response.status_code, 200) #Varmistetaan että sivusto latautuu
        self.assertFalse(response.wsgi_request.user.is_authenticated) #Käyttäjän pitäisi olla uloskirjautuneena

    def test_logout(self):
        #Testataan uloskirjautumista
        self.client.login(username=self.username, password=self.password) #Kirjaudutaan ensin
        response = self.client.post(reverse('base:logout'))
        self.assertEqual(response.status_code, 302)  # Odotetaan uudelleenohjausta uloskirjautumisen jälkeen
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Varmistetaan uloskirjautuminen