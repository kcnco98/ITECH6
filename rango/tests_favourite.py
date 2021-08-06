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


class FavouriteTests(TestCase):

    def test_favourite_class(self):

        self.assertTrue('Page' in dir(rango.models))
        page = rango.models.Page()

        expected_attributes = {
            'learning_list': create_user_object(),
        }

        expected_types = {
            'learning_list': models.fields.related.ManyToManyField,
        }

        found_count = 0

        for attr in page._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name],
                                     f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(page, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()),
                         f"{FAILURE_HEADER}In the Page model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        page.save()


class FavouriteTests(TestCase):

    def test_new_favourite_view_exists(self):
        url = ''

        try:
            url = reverse('rango:learning_list')
        except:
            pass

        self.assertEqual(url, '/rango/learning_list/',
                         f"{FAILURE_HEADER}Have you created the rango:learning_list URL mapping correctly? It should point "
                         f"to the new show_learning_list() view, and have a URL of '/rango/learning_list/' Remember "
                         f"the first part of the URL (/rango/) is handled by the project's urls.py module, "
                         f"and the second part (learning_list/) is handled by the Rango app's urls.py module."
                         f"{FAILURE_FOOTER}")

    def test_favourite_template(self):

        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        template_path = os.path.join(template_base_path, 'learning_list.html')
        self.assertTrue(os.path.exists(template_path),
                        f"{FAILURE_HEADER}We couldn't find the 'learning_list.html' template in the 'templates/rango/' "
                        f"directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)

        ajax_pattern = r'ajax'
        favourite_pattern = r'icobutton icobutton--heart'
        request = self.client.get(reverse('rango:learning_list'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(ajax_pattern, content),
                        f"{FAILURE_HEADER}'ajax' is not correct. Check your learning_list.html template, and try again.{FAILURE_FOOTER}")

        self.assertTrue(re.search(favourite_pattern, template_str),
                        f"{FAILURE_HEADER}Is learninglist.html using 'favourite button'?{FAILURE_FOOTER}")

    def test_favourite_get_response(self):

        request = self.client.get(reverse('rango:learning_list'))
        content = request.content.decode('utf-8')

        self.assertTrue('success: function(response)' in content,
                        f"{FAILURE_HEADER}We couldn't find the 'success: function(response)' "
                        f"in your template. Did you follow the specification in the book to the "
                        f"letter?{FAILURE_FOOTER}")
