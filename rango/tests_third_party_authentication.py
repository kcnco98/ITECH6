import os
import re
import inspect
import tempfile
import rango.models
from rango import forms
from populate_rango import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


def get_template(path_to_template):
    """
    Helper function to return the string representation of a template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str


class ThirdPartyAPITests(TestCase):

    def test_installed_apps(self):
        self.assertTrue('allauth' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.account' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount.providers.google' in settings.INSTALLED_APPS)


class ThirdPartyAuthTests(TestCase):

    def test_third_party_auth_template(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        template_path = os.path.join(template_base_path, 'login.html')
        print(template_base_path)
        print(template_path)
        self.assertTrue(os.path.exists(template_path),
                        f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/rango/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        google_pattern = r'Google'

        request = self.client.get(reverse('rango:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(google_pattern, content),
                        f"{FAILURE_HEADER}The <title> of the response for 'rango:login' is not correct. Check your login.html template, and try again.{FAILURE_FOOTER}")
