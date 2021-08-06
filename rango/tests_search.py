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


class HaystackTests(TestCase):
    """
    A simple test to check whether the auth app has been specified.
    """

    def test_installed_apps(self):
        """
        Checks whether the 'haystack' app has been included in INSTALLED_APPS.
        """
        self.assertTrue('haystack' in settings.INSTALLED_APPS)


class SearchResultTests(TestCase):

    def test_search_template(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'search')
        template_path = os.path.join(template_base_path, 'search.html')
        print(template_base_path)
        print(template_path)
        self.assertTrue(os.path.exists(template_path),
                        f"{FAILURE_HEADER}We couldn't find the 'search.html' template in the 'templates/search/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)Search Result(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Search Result(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('rango:search'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content),
                        f"{FAILURE_HEADER}The <title> of the response for 'rango:search' is not correct. Check your search.html template, and try again.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str),
                        f"{FAILURE_HEADER}Is search.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")

    # def test_search_get_response(self):
    #     request = self.client.get(reverse('rango:search'))
    #     content = request.content.decode('utf-8')
    #
    #     self.assertTrue('Search Result' in content,
    #                     f"{FAILURE_HEADER}We couldn't find the '<h3>Search Result：</h3>' header tag in your search template. Did you follow the specification in the book to the letter?{FAILURE_FOOTER}")
    #     self.assertTrue('{{ result.object.title }}' in content,
    #                     f"{FAILURE_HEADER}When loading the search view with a GET request, we didn't see the required 'object.title'. Check your search.html template and try again.{FAILURE_FOOTER}")

    def test_base_for_search(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        base_path = os.path.join(template_base_path, 'base.html')
        template_str = get_template(base_path)
        self.assertTrue('<form method=\'get\' action="/search/" target="_blank">' in template_str)
