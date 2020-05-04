from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from django.test import TestCase
from .views import signup

# Create your tests here.
class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup')
        self.assertEquals(view.func, signup)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddleware')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

class SuccessfulSignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {
            'username':'jhon',
            'password1':'abcdef123456',
            'password2':'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    def test_redirection(self):
        '''
        A valid form submission should redirect the user the top home
        '''
        self.assertRedirects(self.response, self.home_url)
    
    def test_user_creattion(self):
        self.assertTrue(User.objects.exists())
